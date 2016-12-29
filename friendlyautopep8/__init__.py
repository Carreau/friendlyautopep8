"""
Just a wrapper around autopep8 which run _only_ on the changed (non commited
yet) lines of your files.

"""

import subprocess

__version__ = '0.0.4'


def find_files_and_lines(old=None, new=None):
    import subprocess
    target = []
    if old and new:
        target = ['{old}..{new}'.format(old=old, new=new)]
    elif old:
        target = [str(old)]
    elif new:
        raise ValueError('no clue how to do new only')
    subp = 'git diff -U0'.split(' ') + target

    p = subprocess.Popen(subp, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    lines = [l for l in stdout.decode().splitlines()
             if l.startswith(('+++', '@@'))]
    file_ = None
    chunks = []
    for atline in lines:
        if(atline.startswith('+++ b') or atline == '+++ /dev/null'):
            if file_ is not None:
                yield file_, chunks
            file_ = atline[5:]
            chunks = []
        elif atline.startswith('@@'):
            before, after = atline.split('@@')[1].strip().split(' ')
            if ',' in after:
                start, delta = [int(_) for _ in after.split(',')]
            else:
                start, delta = int(after), 1
            if delta == 0:
                print('skip only deleted lines')
                continue 
            chunks.append((start, start+delta-1))
        else:
            raise ValueError('unknown', atline)
    yield file_, chunks


def main(argv=None):
    import sys
    if not argv:
        argv = sys.argv
    if len(argv) > 2:
        raise ValueError('too many arguments')
    if len(argv) == 2:
        run_on_cwd(argv[1])
    else:
        run_on_cwd()


def run_on_cwd(old=None):

    for fname, linespairs in find_files_and_lines(old=old):
        if not fname.endswith('.py'):
            continue
        for start,stop in linespairs[::-1]:
            torun = 'autopep8 --in-place --line-range'.split() + \
                [str(start), str(stop), '.{}'.format(fname)]
            print(' '.join(torun))
            p = subprocess.Popen(torun, stdout=subprocess.PIPE)
            stdout, stderr = p.communicate()
