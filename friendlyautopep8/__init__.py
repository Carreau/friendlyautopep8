"""
Just a wrapper around autopep8 which run _only_ on the changed (non commited
yet) lines of your files.

"""

import subprocess

__version__ = '0.0.2'



def find_files_and_lines(old=None, new=None):
    import subprocess
    p = subprocess.run('git diff -U0'.split(' '), stdout=subprocess.PIPE)
    lines = [l for l in p.stdout.decode().splitlines() if l.startswith(('+++','@@'))]
    file_ = None
    chunks = []
    for atline in lines:
        if(atline.startswith('+++ b')):
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
            beginning, end = (start, start+delta-1)
            if end < beginning:
                print("Wrong ordering, got", beginning, end, "extracted from", atline, )
            chunks.append((start, start+delta-1))
        else:
            raise ValueError('ubknown', atline)
    yield file_, chunks

def run_on_cwd():
    for fname, linespairs in find_files_and_lines():
        for start,stop in linespairs[::-1]:
            print(' '.join('autopep8 --in-place --line-range'.split()+[str(start),str(stop), '.{}'.format(fname)]))
            subprocess.run('autopep8 --in-place --line-range'.split()+[str(start),str(stop), '.{}'.format(fname)])
