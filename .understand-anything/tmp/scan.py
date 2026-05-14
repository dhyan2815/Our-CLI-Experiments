import os
import sys
import json
import re
from pathlib import Path

project_root = sys.argv[1]
output_path = sys.argv[2]

EXTENSION_MAP = {
    '.ts': 'typescript', '.tsx': 'typescript',
    '.js': 'javascript', '.jsx': 'javascript',
    '.py': 'python',
    '.go': 'go',
    '.rs': 'rust',
    '.java': 'java',
    '.rb': 'ruby',
    '.cpp': 'cpp', '.cc': 'cpp', '.cxx': 'cpp', '.h': 'cpp', '.hpp': 'cpp',
    '.c': 'c',
    '.cs': 'csharp',
    '.swift': 'swift',
    '.kt': 'kotlin',
    '.php': 'php',
    '.vue': 'vue',
    '.svelte': 'svelte',
    '.sh': 'shell', '.bash': 'shell',
    '.ps1': 'powershell',
    '.bat': 'batch', '.cmd': 'batch',
    '.md': 'markdown', '.rst': 'markdown',
    '.yaml': 'yaml', '.yml': 'yaml',
    '.json': 'json', '.jsonc': 'jsonc',
    '.toml': 'toml',
    '.sql': 'sql',
    '.graphql': 'graphql', '.gql': 'graphql',
    '.proto': 'protobuf',
    '.tf': 'terraform', '.tfvars': 'terraform',
    '.html': 'html', '.htm': 'html',
    '.css': 'css', '.scss': 'css', '.sass': 'css', '.less': 'css',
    '.xml': 'xml',
    '.cfg': 'config', '.ini': 'config', '.env': 'config'
}

def get_file_category(file_path):
    ext = Path(file_path).suffix.lower()
    basename = Path(file_path).name.lower()

    if basename in ['dockerfile', 'makefile', 'jenkinsfile', 'procfile', 'vagrantfile'] or \
       basename.startswith('docker-compose') or basename.endswith('.tf') or basename.endswith('.tfvars') or \
       'k8s' in file_path.lower() or 'kubernetes' in file_path.lower() or \
       '.github/workflows' in file_path or basename == '.gitlab-ci.yml' or '.circleci' in file_path:
        return 'infra'

    if ext in ['.sql', '.graphql', '.gql', '.proto', '.prisma'] or file_path.endswith('.schema.json') or ext == '.csv':
        return 'data'

    if ext in ['.sh', '.bash', '.ps1', '.bat', '.cmd']:
        return 'script'

    if ext in ['.html', '.htm', '.css', '.scss', '.sass', '.less']:
        return 'markup'

    if ext in ['.md', '.rst'] and basename != 'license':
        return 'docs'

    if ext in ['.yaml', '.yml', '.json', '.jsonc', '.toml', '.xml', '.cfg', '.ini', '.env'] or \
       basename in ['package.json', 'tsconfig.json', 'pyproject.toml', 'cargo.toml', 'go.mod', 'requirements.txt']:
        return 'config'

    if ext in EXTENSION_MAP:
        return 'code'

    return 'code'

# Discover files using git ls-files
files = []
try:
    import subprocess
    result = subprocess.run(['git', 'ls-files'], cwd=project_root, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        for f in result.stdout.split('\n'):
            f = f.strip()
            if f:
                files.append(f.replace('\\', '/'))
except:
    pass

if not files:
    # Fallback to walk
    excluded_dirs = {'node_modules', '.git', 'vendor', 'venv', '.venv', '__pycache__', '.next', '.cache', '.turbo', 'target', 'obj', 'dist', 'build', 'out', 'coverage'}
    for root, dirs, filenames in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        for f in filenames:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, project_root).replace('\\', '/')
            files.append(rel_path)

# Filter exclusions
exclusion_patterns = [
    r'node_modules/', r'\.git/', r'vendor/', r'venv/', r'\.venv/', r'__pycache__/',
    r'/dist/', r'/build/', r'/out/', r'/coverage/', r'/\.next/', r'/\.cache/', r'/\.turbo/', r'/target/', r'/obj/',
    r'(^|/)bin/',
    r'\.lock$', r'package-lock\.json$', r'yarn\.lock$', r'pnpm-lock\.yaml$',
    r'\.min\.js$', r'\.min\.css$', r'\.map$', r'\.generated\.',
    r'\.ico$', r'\.png$', r'\.jpg$', r'\.jpeg$', r'\.gif$', r'\.svg$', r'\.woff$', r'\.woff2$', r'\.ttf$', r'\.eot$', r'\.mp3$', r'\.mp4$', r'\.pdf$', r'\.zip$', r'\.tar\.gz$',
    r'\.idea/', r'\.vscode/',
    r'^license$', r'\.gitignore$', r'\.editorconfig$', r'\.prettierrc', r'\.eslintrc', r'\.log$',
    r'\.opencode/'
]
excluded_dirs = {'dist', 'build', 'out', 'coverage', '.next', '.cache', '.turbo', 'target', 'obj', '.opencode'}

filtered = []
for f in files:
    segments = f.split('/')
    if any(seg in excluded_dirs for seg in segments):
        continue
    skip = False
    for p in exclusion_patterns:
        if re.search(p, f):
            skip = True
            break
    if not skip:
        filtered.append(f)

original_count = len(files)
files = filtered
filtered_count = original_count - len(files)

# Get file details
file_details = []
for f in files:
    full_path = os.path.join(project_root, f)
    try:
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as fp:
            size_lines = len(fp.readlines())
    except:
        size_lines = 0

    ext = Path(f).suffix.lower()
    if ext in EXTENSION_MAP:
        language = EXTENSION_MAP[ext]
    else:
        basename = Path(f).name.lower()
        if basename == 'dockerfile':
            language = 'dockerfile'
        elif basename == 'makefile':
            language = 'makefile'
        elif basename == 'jenkinsfile':
            language = 'jenkinsfile'
        else:
            language = ext[1:] if ext else 'unknown'

    category = get_file_category(f)
    file_details.append({'path': f, 'language': language, 'sizeLines': size_lines, 'fileCategory': category})

# Detect frameworks
frameworks = set()
file_contents = {}

# Check for various config files
pkg_path = os.path.join(project_root, 'package.json')
if os.path.exists(pkg_path):
    try:
        with open(pkg_path, 'r') as fp:
            pkg = json.load(fp)
        all_deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
        known = ['react', 'vue', 'svelte', '@angular/core', 'express', 'fastify', 'koa', 'next', 'nuxt', 'vite', 'vitest', 'jest', 'mocha', 'tailwindcss', 'prisma', 'typeorm', 'sequelize', 'mongoose', 'redux', 'zustand', 'mobx']
        for dep in all_deps:
            if dep in known:
                name = dep.split('/')[-1] if '/' in dep else dep
                frameworks.add(name[0].upper() + name[1:])
        if pkg.get('name'):
            file_contents['name'] = pkg['name']
        if pkg.get('description'):
            file_contents['description'] = pkg['description']
    except:
        pass

pyproject_path = os.path.join(project_root, 'pyproject.toml')
if os.path.exists(pyproject_path):
    frameworks.add('Python')
    try:
        with open(pyproject_path, 'r') as fp:
            content = fp.read()
            if '[tool.pytest' in content:
                frameworks.add('Pytest')
            if '[tool.django]' in content:
                frameworks.add('Django')
    except:
        pass

req_path = os.path.join(project_root, 'requirements.txt')
if os.path.exists(req_path):
    frameworks.add('Python')

# Infrastructure detection
if any(Path(f).name.lower() == 'dockerfile' for f in files):
    frameworks.add('Docker')
if any('docker-compose.yml' in f or 'docker-compose.yaml' in f for f in files):
    frameworks.add('Docker Compose')
if any(f.endswith('.tf') for f in files):
    frameworks.add('Terraform')
if any('.github/workflows' in f for f in files):
    frameworks.add('GitHub Actions')

# Get unique languages
languages = sorted(set(f['language'] for f in file_details))

# Get project name
if 'name' in file_contents:
    project_name = file_contents['name']
else:
    project_name = os.path.basename(project_root)

# Get README head
readme_head = ''
for name in ['README.md', 'readme.md', 'README.rst', 'readme.rst']:
    full_path = os.path.join(project_root, name)
    if os.path.exists(full_path):
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as fp:
                lines = fp.read().split('\n')[:10]
                readme_head = '\n'.join(lines)
        except:
            pass
        break

# Get import map
import_map = {}
for f in files:
    import_map[f] = []

# Determine complexity
total_files = len(file_details)
if total_files <= 30:
    estimated_complexity = 'small'
elif total_files <= 150:
    estimated_complexity = 'moderate'
elif total_files <= 500:
    estimated_complexity = 'large'
else:
    estimated_complexity = 'very-large'

# Ensure output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Build result
result = {
    'scriptCompleted': True,
    'name': project_name,
    'rawDescription': file_contents.get('description', ''),
    'readmeHead': readme_head,
    'languages': languages,
    'frameworks': list(frameworks),
    'files': sorted(file_details, key=lambda x: x['path']),
    'totalFiles': len(file_details),
    'filteredByIgnore': filtered_count,
    'estimatedComplexity': estimated_complexity,
    'importMap': import_map
}

# Write output
with open(output_path, 'w') as fp:
    json.dump(result, fp, indent=2)

print(f'Scan completed: {total_files} files')
print(f'Languages: {languages}')
print(f'Frameworks: {list(frameworks)}')
print(f'Complexity: {estimated_complexity}')