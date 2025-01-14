#!/usr/bin/env python3

import json
from pathlib import Path
from shutil import copy2, copytree, rmtree
import sys
from typing import Literal

OUR_ROOT = Path(__file__).resolve().parents[1]

# Make relative imports great again
if __name__ == '__main__' and not __package__:
    sys.path.insert(0, str(OUR_ROOT))
    __package__ = 'build'

from .node_app import node_app

FILE_LICENSE = '''
/** This file is part of natlib.
 * https://github.com/mvasilkov/natlib
 * @license MIT | Copyright (c) 2022, 2023 Mark Vasilkov
 */
'use strict'
'''.strip()


def node_modules(binary: Literal['michikoid', 'tsc']) -> Path:
    '''
    Return the path to a binary in the node_modules directory.
    '''
    return OUR_ROOT / 'node_modules' / '.bin' / binary


typescript_check_available, typescript_call = node_app(node_modules('tsc'), ('--version', 'Version (.+?)$', '4'))
_, michikoid_call = node_app(node_modules('michikoid'))


def natlib_clean():
    package_dir = OUR_ROOT / 'out'
    if package_dir.is_dir():
        rmtree(package_dir)

    tsc_cache = OUR_ROOT / 'tsconfig.tsbuildinfo'
    if tsc_cache.is_file():
        tsc_cache.unlink()

    assert not package_dir.exists()


def natlib_build():
    typescript_call(['--project', OUR_ROOT])

    files = list(OUR_ROOT.glob('out/**/*.js'))
    michikoid_call(files)


def natlib_package():
    package_dir = OUR_ROOT / 'out'

    contents = (
        ('typescript', 'typescript'),
        ('LICENSE', 'LICENSE'),
        ('README.md', 'README.md'),
        ('tsconfig.json', 'tsconfig.json'),
    )

    for path_str, target_str in contents:
        path = OUR_ROOT / path_str
        target_path = package_dir / target_str
        assert not target_path.exists()
        if path.is_dir():
            copytree(path, target_path)
        else:
            copy2(path, target_path)

    copy_package_json()


def copy_package_json():
    infile = OUR_ROOT / 'package.json'
    outfile = OUR_ROOT / 'out' / 'package.json'
    options = {
        'ensure_ascii': False,
        'allow_nan': False,
        'indent': 2,
    }
    content = json.loads(infile.read_text(encoding='utf-8'))
    del content['scripts']['prepublishOnly']
    del content['devDependencies']
    del content['private']
    content_str = json.dumps(content, **options)
    if not content_str.endswith('\n'):
        content_str += '\n'
    outfile.write_text(content_str, encoding='utf-8', newline='\n')


def natlib_validate():
    for file in list(OUR_ROOT.glob('out/**/*.js')):
        content = file.read_text(encoding='utf-8')
        if not content.startswith(FILE_LICENSE):
            raise RuntimeError(f'Bad file header: {file.relative_to(OUR_ROOT)}')


if __name__ == '__main__':
    typescript_check_available()

    print('natlib: clean')
    natlib_clean()

    if sys.argv[1:] == ['clean']:
        sys.exit()

    print('natlib: build')
    natlib_build()

    print('natlib: package')
    natlib_package()

    print('natlib: validate')
    natlib_validate()
