import os
import sys
import json
import re
from pathlib import Path

project_root = sys.argv[1]
output_path = sys.argv[2]

# Language detection mapping
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

    # Infra patterns
    if basename in ['dockerfile', 'makefile', 'jenkinsfile', 'procfile', 'vagrantfile'] or \
       basename.startswith('docker-compose') or basename.endswith('.tf') or basename.endswith('.tfvars') or \
       'k8s' in file_path.lower() or 'kubernetes' in file_path.lower() or \
       '.github/workflows' in file_path or basename == '.gitlab-ci.yml' or '.circleci' in file_path:
        return 'infra'

    # Data patterns
    if ext in ['.sql', '.graphql', '.gql', '.proto', '.prisma'] or file_path.endswith('.schema.json') or ext == '.csv':
        return 'data'

    # Script patterns
    if ext in ['.sh', '.bash', '.ps1', '.bat', '.cmd']:
        return 'script'

    # Markup patterns
    if ext in ['.html', '.htm', '.css', '.scss', '.sass', '.less']:
        return 'markup'

    # Docs patterns
    if ext in ['.md', '.rst'] and basename != 'license':
        return 'docs'

    # Config patterns
    if ext in ['.yaml', '.yml', '.json', '.jsonc', '.toml', '.xml', '.cfg', '.ini', '.env'] or \
       basename in ['package.json', 'tsconfig.json', 'pyproject.toml', 'cargo.toml', 'go.mod', 'requirements.txt']:
        return 'config'

    # Default to code for known code extensions
    if ext in EXTENSION_MAP:
        return 'code'

    return 'code'

def discover_files():
    files = []
    try:
        # Try git ls-files
        import subprocess
        result = subprocess.run(['git', 'ls-files'], cwd=project_root, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            for f in result.stdout.split('\n'):
                f = f.strip()
                if f:
                    files.append(f.replace('\\', '/'))
            return files
    except:
        pass

    # Fallback to recursive walk
    excluded_dirs = {'node_modules', '.git', 'vendor', 'venv', '.venv', '__pycache__', '.next', '.cache', '.turbo', 'target', 'obj'}
    for root, dirs, filenames in os.walk(project_root):
        # Filter excluded directories in-place
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        for f in filenames:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, project_root).replace('\\', '/')
            files.append(rel_path)
    return files

def filter_exclusions(files):
    exclusion_patterns = [
        r'node_modules/', r'\.git/', r'vendor/', r'venv/', r'\.venv/', r'__pycache__/',
        r'/dist/', r'/build/', r'/out/', r'/coverage/', r'/\.next/', r'/\.cache/', r'/\.turbo/', r'/target/', r'/obj/',
        r'(^|/)bin/',
        r'\.lock$', r'package-lock\.json$', r'yarn\.lock$', r'pnpm-lock\.yaml$',
        r'\.min\.js$', r'\.min\.css$', r'\.map$', r'\.generated\.',
        r'\.ico$', r'\.png$', r'\.jpg$', r'\.jpeg$', r'\.gif$', r'\.svg$', r'\.woff$', r'\.woff2$', r'\.ttf$', r'\.eot$', r'\.mp3$', r'\.mp4$', r'\.pdf$', r'\.zip$', r'\.tar\.gz$',
        r'\.idea/', r'\.vscode/',
        r'^license$', r'\.gitignore$', r'\.editorconfig$', r'\.prettierrc', r'\.eslintrc', r'\.log$'
    ]
    excluded_dirs = {'dist', 'build', 'out', 'coverage', '.next', '.cache', '.turbo', 'target', 'obj'}

    filtered = []
    for f in files:
        # Check directory segments
        segments = f.split('/')
        if any(seg in excluded_dirs for seg in segments):
            continue

        # Check patterns
        skip = False
        for p in exclusion_patterns:
            if re.search(p, f):
                skip = True
                break
        if not skip:
            filtered.append(f)
    return filtered

def get_language(file_path):
    ext = Path(file_path).suffix.lower()
    if ext in EXTENSION_MAP:
        return EXTENSION_MAP[ext]

    basename = Path(file_path).name.lower()
    if basename == 'dockerfile':
        return 'dockerfile'
    if basename == 'makefile':
        return 'makefile'
    if basename == 'jenkinsfile':
        return 'jenkinsfile'

    return ext[1:] if ext else 'unknown'

def count_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return len(f.readlines())
    except:
        return 0

def detect_frameworks(files):
    frameworks = set()
    file_contents = {}

    # Check package.json
    pkg_path = os.path.join(project_root, 'package.json')
    if os.path.exists(pkg_path):
        try:
            with open(pkg_path, 'r') as f:
                pkg = json.load(f)
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

    # Check Cargo.toml
    cargo_path = os.path.join(project_root, 'Cargo.toml')
    if os.path.exists(cargo_path):
        frameworks.add('Rust')
        try:
            with open(cargo_path, 'r') as f:
                content = f.read()
                match = re.search(r'name\s*=\s*"([^"]+)"', content)
                if match:
                    file_contents['cargoName'] = match.group(1)
        except:
            pass

    # Check go.mod
    go_path = os.path.join(project_root, 'go.mod')
    if os.path.exists(go_path):
        frameworks.add('Go')
        try:
            with open(go_path, 'r') as f:
                content = f.read()
                match = re.search(r'module\s+([^\s]+)', content)
                if match:
                    file_contents['goModule'] = match.group(1)
        except:
            pass

    # Check pyproject.toml
    pyproject_path = os.path.join(project_root, 'pyproject.toml')
    if os.path.exists(pyproject_path):
        frameworks.add('Python')
        try:
            with open(pyproject_path, 'r') as f:
                content = f.read()
                if '[tool.pytest' in content:
                    frameworks.add('Pytest')
                if '[tool.django]' in content:
                    frameworks.add('Django')
        except:
            pass

    # Check requirements.txt
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
    if any(f == '.gitlab-ci.yml' for f in files):
        frameworks.add('GitLab CI')
    if any(f == 'jenkinsfile' for f in files):
        frameworks.add('Jenkins')

    return frameworks, file_contents

def get_project_name(file_contents, project_root):
    if 'name' in file_contents:
        return file_contents['name']
    if 'cargoName' in file_contents:
        return file_contents['cargoName']
    if 'goModule' in file_contents:
        return file_contents['goModule'].split('/')[-1]

    # Try pyproject.toml
    pyproject_path = os.path.join(project_root, 'pyproject.toml')
    if os.path.exists(pyproject_path):
        try:
            with open(pyproject_path, 'r') as f:
                content = f.read()
                match = re.search(r'name\s*=\s*"([^"]+)"', content)
                if match:
                    return match.group(1)
        except:
            pass

    return os.path.basename(project_root)

def get_readme_head(files):
    for name in ['README.md', 'readme.md', 'README.rst', 'readme.rst']:
        full_path = os.path.join(project_root, name)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.read().split('\n')[:10]
                    return '\n'.join(lines)
            except:
                pass
    return ''

def resolve_imports(files, file_category_map):
    import_map = {}
    code_files = [f for f in files if file_category_map.get(f) == 'code']
    file_set = set(files)

    for file_path in code_files:
        import_map[file_path] = []
        full_path = os.path.join(project_root, file_path)
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            ext = Path(file_path).suffix.lower()

            if ext in ['.ts', '.tsx', '.js', '.jsx']:
                # JS/TS imports
                for match in re.finditer(r(?:import\s+.*?\s+from\s+['"](\.[^'"]+)['"]|require\s*\(\s*['"](\.[^'"]+)['"]\s*\)), content):
                    imp = match.group(1) or match.group(2)
                    resolved = resolve_path(file_path, imp, files)
                    if resolved:
                        import_map[file_path].append(resolved)
            elif ext == '.py':
                # Python imports
                for match in re.finditer(r(?:from\s+([\w.]+)\s+import|import\s+([\w.]+)), content):
                    module = match.group(1) or match.group(2)
                    if not module.startswith('.'):
                        resolved = resolve_python_import(module, files)
                        import_map[file_path].extend(resolved)
                    else:
                        resolved = resolve_path(file_path, module, files)
                        if resolved:
                            import_map[file_path].append(resolved)
        except:
            pass

    return import_map

def resolve_path(file_path, import_path, files):
    dir_path = os.path.dirname(file_path)
    resolved = os.path.join(dir_path, import_path).replace('\\', '/')
    if resolved in files:
        return resolved

    exts = ['', '.ts', '.tsx', '.js', '.jsx', '.py', '/index.ts', '/index.js', '/index.tsx', '/index.jsx']
    for ext in exts:
        trial = resolved + ext
        if trial in files:
            return trial
    return None

def resolve_python_import(module, files):
    results = []
    parts = module.split('.')
    module_path = '/'.join(parts) + '.py'
    if module_path in files:
        results.append(module_path)
    package_path = '/'.join(parts) + '/__init__.py'
    if package_path in files:
        results.append(package_path)
    return results

# Main
try:
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Discover files
    files = discover_files()
    original_count = len(files)

    # Filter exclusions
    files = filter_exclusions(files)
    filtered_count = original_count - len(files)

    # Get file details
    file_details = []
    for f in files:
        full_path = os.path.join(project_root, f)
        size_lines = count_lines(full_path)
        language = get_language(f)
        category = get_file_category(f)
        file_details.append({'path': f, 'language': language, 'sizeLines': size_lines, 'fileCategory': category})

    # Detect frameworks
    frameworks, file_contents = detect_frameworks(files)

    # Get unique languages
    languages = sorted(set(f['language'] for f in file_details))

    # Get project name
    project_name = get_project_name(file_contents, project_root)

    # Get README head
    readme_head = get_readme_head(files)

    # Get import map
    file_category_map = {f['path']: f['fileCategory'] for f in file_details}
    import_map = resolve_imports(files, file_category_map)

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
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print('Scan completed successfully')
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)