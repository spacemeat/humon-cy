''' Builds against a version of the Humon C library.'''

from pathlib import Path
import subprocess
import sys

__version__ = '(unknown version)'
version_tuple = (0, 0, '(unknown version)')

OFF = '\033[0m'
BRIGHT_BLACK_FG = '\033[90m'
BRIGHT_RED_FG = '\033[91m'

# map humon-py to humon version numbers
VERSION_MAP = {
    '(unknown version)': 'v0.2.1',
    'v0.1.0': 'v0.2.1'
}

URL = 'https://api.github.com/repos/spacemeat/humon/tarball/{version}'
REPO_NAME = 'humon-{version}'
TARBALL_NAME = f'{REPO_NAME}.tar.gz'
LINK_NAME = 'humon'
CURL_CMD = f'curl -L -H "Accept: application/vnd.github+json" {URL} --output clib/{TARBALL_NAME}'
MKDIR_CLIB_CMD = 'mkdir -p clib'
MKDIR_REPO_CMD = f'mkdir -p clib/{REPO_NAME}'
EXPAND_CMD = f'tar -xf clib/{TARBALL_NAME} -C clib/{REPO_NAME} --strip-components=1'
UNLINK_CMD = f'unlink clib/{LINK_NAME}'
LINK_CMD = f'ln -s {REPO_NAME} clib/{LINK_NAME}'

def do_shell_command(cmd):
    ''' Perorm an arbitrary shell command in a subprocess.'''
    print (f'{BRIGHT_BLACK_FG}{cmd}{OFF}')
    cs = subprocess.run(cmd, shell=True, check=True)
    if cs.returncode != 0:
        print (f'{BRIGHT_RED_FG}{cs.stderr}{OFF}')
    else:
        print (f'{cs.stdout or ""}')
    return cs.returncode, cs.stdout or '', cs.stderr or ''

def get_repo(version):
    ''' Pulls the tagged repo from github if it needs to, and softlinks from clib/humon. '''
    repo_name       = REPO_NAME.format(version = version)
    tarball_name    = TARBALL_NAME.format(version = version)
    mkdir_repo_cmd  = MKDIR_REPO_CMD.format(version = version)
    curl_cmd        = CURL_CMD.format(version = version)
    expand_cmd      = EXPAND_CMD.format(version = version)
    unlink_cmd      = UNLINK_CMD.format(version = version)
    link_cmd        = LINK_CMD.format(version = version)

    if not Path('clib').exists():
        if do_shell_command(MKDIR_CLIB_CMD)[0] != 0:
            raise RuntimeError(mkdir_repo_cmd)

    if Path(f'clib/{LINK_NAME}').is_symlink():
        if do_shell_command(unlink_cmd)[0] != 0:
            raise RuntimeError(unlink_cmd)

    if not Path(f'clib/{tarball_name}').exists():
        if do_shell_command(curl_cmd)[0] != 0:
            raise RuntimeError(curl_cmd)

    if not Path(f'clib/{repo_name}').is_dir():
        if do_shell_command(mkdir_repo_cmd)[0] != 0:
            raise RuntimeError(mkdir_repo_cmd)

    if not Path(f'clib/{repo_name}/LICENSE').exists():
        if do_shell_command(expand_cmd)[0] != 0:
            raise RuntimeError(expand_cmd)

    if do_shell_command(link_cmd)[0] != 0:
        raise RuntimeError(link_cmd)


def main():
    ''' Mane. '''
    c_library_version = VERSION_MAP.get(__version__, 'main')
    get_repo(c_library_version)

    build_cmd = 'python3 -m build'
    ret, _, _= do_shell_command(build_cmd)
    if ret != 0:
        raise RuntimeError(build_cmd)

    return 0

if __name__ == "__main__":
    sys.exit(main())
