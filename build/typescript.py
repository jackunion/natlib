import platform
import re
from subprocess import check_call, check_output

REQUIRE_SHELL = platform.system() == 'Windows'


def typescript_check_available():
    try:
        result = check_output(['tsc', '--version'], encoding='utf-8', shell=REQUIRE_SHELL)
    except FileNotFoundError:
        raise RuntimeError('Cannot run `tsc` (FileNotFoundError)')

    version = re.match(r'Version (.+?)$', result, re.MULTILINE)
    if version is None:
        raise RuntimeError(f'Cannot understand `tsc --version`, got {result!r}')

    version_tuple = tuple(version.group(1).split('.'))
    if version_tuple[0] != '4':
        raise RuntimeError(f'Expected tsc version 4, got {version.group(1)!r}')

    return version_tuple


def typescript_call(args: list):
    try:
        check_call(['tsc'] + args, shell=REQUIRE_SHELL)
    except FileNotFoundError:
        raise RuntimeError('Cannot run `tsc` (FileNotFoundError)')