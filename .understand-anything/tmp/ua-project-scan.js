const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const projectRoot = process.argv[2];
const outputPath = process.argv[3];

if (!projectRoot || !outputPath) {
  console.error('Usage: node script.js <project-root> <output-path>');
  process.exit(1);
}

// Language detection mapping
const EXTENSION_MAP = {
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
};

// File category detection
function getFileCategory(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const basename = path.basename(filePath).toLowerCase();

  // Infra patterns
  if (basename === 'dockerfile' || basename.startsWith('docker-compose') ||
      basename === 'makefile' || basename === 'jenkinsfile' || basename === 'procfile' ||
      basename === 'vagrantfile' || basename === 'terraform' || basename.endsWith('.tf') ||
      basename.endsWith('.tfvars') || basename.includes('k8s') ||
      filePath.includes('k8s/') || filePath.includes('kubernetes/') ||
      filePath.includes('.github/workflows/') || basename === '.gitlab-ci.yml' ||
      basename.includes('.circleci/')) {
    return 'infra';
  }

  // Data patterns
  if (['.sql', '.graphql', '.gql', '.proto', '.prisma', '.schema.json', '.csv'].includes(ext)) {
    return 'data';
  }

  // Script patterns
  if (['.sh', '.bash', '.ps1', '.bat', '.cmd'].includes(ext)) {
    return 'script';
  }

  // Markup patterns
  if (['.html', '.htm', '.css', '.scss', '.sass', '.less'].includes(ext)) {
    return 'markup';
  }

  // Docs patterns
  if (['.md', '.rst'].includes(ext) && basename !== 'license') {
    return 'docs';
  }

  // Config patterns
  if (['.yaml', '.yml', '.json', '.jsonc', '.toml', '.xml', '.cfg', '.ini', '.env'].includes(ext) ||
      ['package.json', 'tsconfig.json', 'pyproject.toml', 'cargo.toml', 'go.mod', 'requirements.txt'].includes(basename)) {
    return 'config';
  }

  // Default to code for known code extensions
  if (Object.keys(EXTENSION_MAP).includes(ext)) {
    return 'code';
  }

  return 'code'; // Default
}

// Step 1: File discovery
function discoverFiles() {
  try {
    // Try git ls-files first
    const gitFiles = execSync('git ls-files', { cwd: projectRoot, encoding: 'utf8', timeout: 30000 });
    return gitFiles.split('\n').filter(f => f.trim()).map(f => f.replace(/\\/g, '/'));
  } catch (e) {
    // Fallback to recursive walk
    const files = [];
    function walk(dir) {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name).replace(/\\/g, '/');
        if (entry.isDirectory()) {
          if (!['node_modules', '.git', 'vendor', 'venv', '.venv', '__pycache__', '.next', '.cache', '.turbo', 'target'].includes(entry.name)) {
            walk(fullPath);
          }
        } else {
          files.push(fullPath);
        }
      }
    }
    walk(projectRoot);
    return files.map(f => path.relative(projectRoot, f).replace(/\\/g, '/'));
  }
}

// Step 2: Exclusion filtering
function filterExclusions(files) {
  const exclusionPatterns = [
    /node_modules\//, /\.git\//, /vendor\//, /venv\//, /\.venv\//, /__pycache__\//,
    /\/dist\//, /\/build\//, /\/out\//, /\/coverage\//, /\.next\//, /\.cache\//, /\.turbo\//, /\/target\//, /\/obj\//,
    /(^|\/)bin\//, /\/obj\//,
    /\.lock$/, /package-lock\.json$/, /yarn\.lock$/, /pnpm-lock\.yaml$/,
    /\.min\.js$/, /\.min\.css$/, /\.map$/, /\.generated\./,
    /\.ico$/, /\.png$/, /\.jpg$/, /\.jpeg$/, /\.gif$/, /\.svg$/, /\.woff$/, /\.woff2$/, /\.ttf$/, /\.eot$/, /\.mp3$/, /\.mp4$/, /\.pdf$/, /\.zip$/, /\.tar\.gz$/,
    /\.idea\//, /\.vscode\//,
    /^license$/i, /\.gitignore$/, /\.editorconfig$/, /\.prettierrc/, /\.eslintrc/, /\.log$/
  ];

  return files.filter(f => {
    const normalized = f.replace(/\\/g, '/');
    // Check directory segments (for build/ dist/ etc)
    const segments = normalized.split('/');
    const hasExcludedDir = segments.some(seg => ['dist', 'build', 'out', 'coverage', '.next', '.cache', '.turbo', 'target', 'obj'].includes(seg));

    return !exclusionPatterns.some(p => p.test(normalized)) && !hasExcludedDir;
  });
}

// Get language from extension
function getLanguage(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const lang = EXTENSION_MAP[ext];
  if (lang) return lang;

  // Special cases for no-extension files
  const basename = path.basename(filePath).toLowerCase();
  if (basename === 'dockerfile') return 'dockerfile';
  if (basename === 'makefile') return 'makefile';
  if (basename === 'jenkinsfile') return 'jenkinsfile';

  // Fallback to extension without dot, or unknown
  return ext ? ext.slice(1) : 'unknown';
}

// Count lines in a file
function countLines(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    return content.split('\n').length;
  } catch (e) {
    return 0;
  }
}

// Read config files for framework detection
function detectFrameworks(files) {
  const frameworks = new Set();
  const fileContents = {};

  // Read package.json
  const pkgPath = path.join(projectRoot, 'package.json');
  if (fs.existsSync(pkgPath)) {
    try {
      const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
      const allDeps = { ...pkg.dependencies, ...pkg.devDependencies };
      const knownFrameworks = ['react', 'vue', 'svelte', '@angular/core', 'express', 'fastify', 'koa', 'next', 'nuxt', 'vite', 'vitest', 'jest', 'mocha', 'tailwindcss', 'prisma', 'typeorm', 'sequelize', 'mongoose', 'redux', 'zustand', 'mobx'];
      Object.keys(allDeps).forEach(dep => {
        if (knownFrameworks.includes(dep)) {
          const name = dep.startsWith('@') ? dep.split('/')[1] : dep;
          frameworks.add(name.charAt(0).toUpperCase() + name.slice(1));
        }
      });
      if (pkg.name) fileContents['name'] = pkg.name;
      if (pkg.description) fileContents['description'] = pkg.description;
    } catch (e) {}
  }

  // Check Cargo.toml
  const cargoPath = path.join(projectRoot, 'Cargo.toml');
  if (fs.existsSync(cargoPath)) {
    frameworks.add('Rust');
    try {
      const content = fs.readFileSync(cargoPath, 'utf8');
      const nameMatch = content.match(/name\s*=\s*"([^"]+)"/);
      if (nameMatch) fileContents['cargoName'] = nameMatch[1];
    } catch (e) {}
  }

  // Check go.mod
  const goPath = path.join(projectRoot, 'go.mod');
  if (fs.existsFile(goPath)) {
    frameworks.add('Go');
    try {
      const content = fs.readFileSync(goPath, 'utf8');
      const modMatch = content.match(/module\s+([^\s]+)/);
      if (modMatch) fileContents['goModule'] = modMatch[1];
    } catch (e) {}
  }

  // Check pyproject.toml
  const pyprojectPath = path.join(projectRoot, 'pyproject.toml');
  if (fs.existsSync(pyprojectPath)) {
    frameworks.add('Python');
    try {
      const content = fs.readFileSync(pyprojectPath, 'utf8');
      if (content.includes('[tool.pytest')) frameworks.add('Pytest');
      if (content.includes('[tool.django]')) frameworks.add('Django');
    } catch (e) {}
  }

  // Check requirements.txt
  const reqPath = path.join(projectRoot, 'requirements.txt');
  if (fs.existsSync(reqPath)) {
    frameworks.add('Python');
  }

  // Infrastructure detection
  if (files.some(f => path.basename(f).toLowerCase() === 'dockerfile')) frameworks.add('Docker');
  if (files.some(f => f.includes('docker-compose.yml') || f.includes('docker-compose.yaml'))) frameworks.add('Docker Compose');
  if (files.some(f => f.endsWith('.tf'))) frameworks.add('Terraform');
  if (files.some(f => f.includes('.github/workflows/'))) frameworks.add('GitHub Actions');
  if (files.some(f => f === '.gitlab-ci.yml')) frameworks.add('GitLab CI');
  if (files.some(f => f === 'jenkinsfile')) frameworks.add('Jenkins');

  return { frameworks: Array.from(frameworks), fileContents };
}

// Get project name
function getProjectName(fileContents, files) {
  if (fileContents.name) return fileContents.name;
  if (fileContents.cargoName) return fileContents.cargoName;
  if (fileContents.goModule) return fileContents.goModule.split('/').pop();

  // Try pyproject.toml
  const pyprojectPath = path.join(projectRoot, 'pyproject.toml');
  if (fs.existsSync(pyprojectPath)) {
    try {
      const content = fs.readFileSync(pyprojectPath, 'utf8');
      const nameMatch = content.match(/name\s*=\s*"([^"]+)"/);
      if (nameMatch) return nameMatch[1];
    } catch (e) {}
  }

  // Fallback to directory name
  return path.basename(projectRoot);
}

// Get README content
function getReadmeHead(files) {
  const readmePaths = ['README.md', 'readme.md', 'README.rst', 'readme.rst'];
  for (const rp of readmePaths) {
    const fullPath = path.join(projectRoot, rp);
    if (fs.existsSync(fullPath)) {
      try {
        const content = fs.readFileSync(fullPath, 'utf8');
        const lines = content.split('\n').slice(0, 10).join('\n');
        return lines;
      } catch (e) {}
    }
  }
  return '';
}

// Resolve imports for code files
function resolveImports(files, fileCategoryMap) {
  const importMap = {};
  const codeFiles = files.filter(f => fileCategoryMap[f] === 'code');

  // Build a set for quick lookup
  const fileSet = new Set(files);

  // Read tsconfig for path aliases
  let pathAliases = {};
  const tsconfigPath = path.join(projectRoot, 'tsconfig.json');
  if (fs.existsSync(tsconfigPath)) {
    try {
      const tsconfig = JSON.parse(fs.readFileSync(tsconfigPath, 'utf8'));
      if (tsconfig.compilerOptions?.paths) {
        pathAliases = tsconfig.compilerOptions.paths;
      }
    } catch (e) {}
  }

  codeFiles.forEach(filePath => {
    importMap[filePath] = [];
    const fullPath = path.join(projectRoot, filePath);
    try {
      const content = fs.readFileSync(fullPath, 'utf8');
      const ext = path.extname(filePath).toLowerCase();

      if (['.ts', '.tsx', '.js', '.jsx'].includes(ext)) {
        // JavaScript/TypeScript imports
        const relativeRegex = /(?:import\s+.*?\s+from\s+['"](\.[^'"]+)['"]|require\s*\(\s*['"](\.[^'"]+)['"]\s*\))/g;
        let match;
        while ((match = relativeRegex.exec(content)) !== null) {
          const importPath = match[1] || match[2];
          const resolved = resolvePath(filePath, importPath, files);
          if (resolved) importMap[filePath].push(resolved);
        }
      } else if (ext === '.py') {
        // Python imports
        const pyRegex = /(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))/g;
        let match;
        while ((match = pyRegex.exec(content)) !== null) {
          const module = match[1] || match[2];
          if (!module.startsWith('.')) {
            // Absolute import - try to resolve
            const resolved = resolvePythonImport(module, filePath, files);
            if (resolved) importMap[filePath].push(...resolved);
          } else {
            // Relative import
            const resolved = resolvePath(filePath, module, files);
            if (resolved) importMap[filePath].push(resolved);
          }
        }
      }
    } catch (e) {
      // Skip files that can't be read
    }
  });

  return importMap;
}

// Resolve relative path with extension variants
function resolvePath(filePath, importPath, files) {
  const dir = path.dirname(filePath);
  let resolved;

  // Try as-is
  resolved = path.join(dir, importPath).replace(/\\/g, '/');
  if (files.includes(resolved)) return resolved;

  // Try with extensions
  const exts = ['', '.ts', '.tsx', '.js', '.jsx', '.py', '/index.ts', '/index.js', '/index.tsx', '/index.jsx'];
  for (const ext of exts) {
    const trial = resolved + ext;
    if (files.includes(trial)) return trial;
  }

  return null;
}

// Resolve Python absolute imports
function resolvePythonImport(module, filePath, files) {
  const results = [];
  const parts = module.split('.');

  // Try as module file
  const modulePath = parts.join('/') + '.py';
  if (files.includes(modulePath)) results.push(modulePath);

  // Try as package
  const packagePath = parts.join('/') + '/__init__.py';
  if (files.includes(packagePath)) results.push(packagePath);

  return results;
}

// Main execution
try {
  // Ensure output directory exists
  const outputDir = path.dirname(outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Discover files
  let files = discoverFiles();
  const originalCount = files.length;

  // Filter exclusions
  files = filterExclusions(files);
  const filteredCount = originalCount - files.length;

  // Get file details
  const fileDetails = files.map(f => {
    const fullPath = path.join(projectRoot, f);
    const sizeLines = countLines(fullPath);
    const language = getLanguage(f);
    const category = getFileCategory(f);
    return { path: f, language, sizeLines, fileCategory: category };
  });

  // Detect frameworks
  const { frameworks, fileContents } = detectFrameworks(files);

  // Get unique languages
  const languages = [...new Set(fileDetails.map(f => f.language))].sort();

  // Get project name
  const projectName = getProjectName(fileContents, files);

  // Get README head
  const readmeHead = getReadmeHead(files);

  // Get import map
  const fileCategoryMap = {};
  fileDetails.forEach(f => fileCategoryMap[f.path] = f.fileCategory);
  const importMap = resolveImports(files, fileCategoryMap);

  // Determine complexity
  let estimatedComplexity;
  const totalFiles = fileDetails.length;
  if (totalFiles <= 30) estimatedComplexity = 'small';
  else if (totalFiles <= 150) estimatedComplexity = 'moderate';
  else if (totalFiles <= 500) estimatedComplexity = 'large';
  else estimatedComplexity = 'very-large';

  // Build result
  const result = {
    scriptCompleted: true,
    name: projectName,
    rawDescription: fileContents.description || '',
    readmeHead,
    languages,
    frameworks,
    files: fileDetails.sort((a, b) => a.path.localeCompare(b.path)),
    totalFiles: fileDetails.length,
    filteredByIgnore: filteredCount,
    estimatedComplexity,
    importMap
  };

  // Write output
  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2));
  console.log('Scan completed successfully');
  process.exit(0);
} catch (e) {
  console.error('Error:', e.message);
  console.error(e.stack);
  process.exit(1);
}