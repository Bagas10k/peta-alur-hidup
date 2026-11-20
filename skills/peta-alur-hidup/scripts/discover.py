"""Read-only project inventory: paths only, no imports, no repository code execution."""
import argparse
import json
import os
from pathlib import Path

SKIP = {'.git', '.hg', '.svn', 'node_modules', 'vendor', 'dist', 'build', 'target', 'out', 'coverage', 'bin', 'obj', 'storage', 'tmp', 'secrets', 'credentials', 'backups', 'fixtures', 'testdata', '__pycache__', 'venv', 'env', 'site-packages'}
MANIFESTS = {'package.json': 'JavaScript/TypeScript', 'composer.json': 'PHP', 'pyproject.toml': 'Python', 'requirements.txt': 'Python', 'go.mod': 'Go', 'Cargo.toml': 'Rust', 'pom.xml': 'Java', 'build.gradle': 'JVM', 'Gemfile': 'Ruby', 'pubspec.yaml': 'Dart'}
EXT = {'.py', '.js', '.jsx', '.ts', '.tsx', '.mjs', '.go', '.rs', '.php', '.java', '.kt', '.rb', '.cs', '.swift', '.dart', '.vue', '.svelte'}
SIGNALS = ('route', 'controller', 'workflow', 'handler', 'command', 'service', 'state', 'task', 'event', 'listener', 'worker', 'policy', 'main', 'model', 'app')

def eligible(p):
    return not (p.name.startswith('.') or p.name.lower() in SKIP or p.is_symlink() or getattr(p, 'is_junction', lambda: False)())

def scan(root, limit=80, budget=10000):
    if not root.is_dir():
        raise ValueError('Folder proyek tidak ditemukan')
    entries, manifests, languages, skipped = [], [], {}, []
    seen = 0
    truncated = False
    for base, dirs, files in os.walk(root, followlinks=False, onerror=lambda exc: skipped.append(Path(exc.filename).name)):
        folder = Path(base)
        dirs[:] = sorted(n for n in dirs if eligible(folder/n))
        for n in sorted(files):
            p = folder/n
            seen += 1
            if seen > budget:
                truncated = True
                break
            if not eligible(p) or not p.is_file():
                continue
            rel = p.relative_to(root).as_posix()
            if n in MANIFESTS or p.suffix == '.csproj':
                manifests.append({'path': rel, 'stack_hint': MANIFESTS.get(n, '.NET')})
            ext = p.suffix.lower()
            if ext not in EXT or any(x in n.lower() for x in ('.min.', '.generated.', 'credential', 'secret', 'private_key')):
                continue
            languages[ext] = languages.get(ext, 0) + 1
            score = sum(x in rel.lower() for x in SIGNALS) - 4 * any(x in rel.lower() for x in ('/test', 'tests/', '.spec.', '_test.'))
            entries.append((-score, len(p.parts), rel))
        if truncated:
            break
    return {'manifests': manifests, 'source_counts': dict(sorted(languages.items())), 'candidates': [r for _, _, r in sorted(entries)[:limit]], 'more_candidates': len(entries) > limit, 'scan_truncated': truncated, 'unreadable_dirs': skipped}

if __name__ == '__main__':
    arg = argparse.ArgumentParser(description=__doc__)
    arg.add_argument('root', type=Path)
    args = arg.parse_args()
    try:
        print(json.dumps(scan(args.root), indent=2, ensure_ascii=True))
    except (OSError, ValueError) as exc:
        arg.exit(2, str(exc) + '\n')
