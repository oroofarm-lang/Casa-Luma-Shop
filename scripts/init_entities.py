#!/usr/bin/env python3
"""Create basic entity files without overwriting existing content.

Usage: python3 scripts/init_entities.py [entity-name ...]
With no names, use existing entity directories and the identified Casa Luma project.
"""

import argparse
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('names', nargs='*', help='Entity folder names, e.g. casa-luma')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    entities = root / 'entities'
    names = args.names or sorted(
        {'casa-luma'} | {p.name for p in entities.iterdir() if p.is_dir()}
        if entities.exists() else {'casa-luma'}
    )
    # Validate every name before making any changes.
    for name in names:
        if not re.fullmatch(r'[\w][\w-]*', name):
            parser.error(f'Invalid entity name: {name!r}')
        target = entities / name
        if not target.resolve().is_relative_to(root.resolve()):
            parser.error(f'Entity path escapes project: {name!r}')

    created = 0
    preserved = 0
    for name in dict.fromkeys(names):
        folder = entities / name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'files').mkdir(exist_ok=True)
        templates = {
            'context.md': f'# {name} — Context\n\n## Background\n\n## Business purpose\n\n## Decisions\n',
            'memory.md': f'# {name} — Memory\n\n## Stable facts\n\n## Technical details\n',
            'tasks.md': f'# {name} — Tasks\n\n## To do\n\n## In progress\n\n## Done\n',
        }
        for filename, content in templates.items():
            path = folder / filename
            try:
                with path.open('x', encoding='utf-8') as handle:
                    handle.write(content)
                created += 1
                print(f'Created: {path.relative_to(root)}')
            except FileExistsError:
                preserved += 1
                print(f'Preserved: {path.relative_to(root)}')
        print(f'Ready: {(folder / "files").relative_to(root)}/')
    print(f'Entities: {len(set(names))}; files created: {created}; preserved: {preserved}')


if __name__ == '__main__':
    main()
