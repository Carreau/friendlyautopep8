# Friendly autopep8

A wrapper around [autopep8] which rums it only on non commited lines. I.E run
`git-diff` between the worktree and this index and apply autopep8 only to
there. 

## Usage

### Commandline:

```
$ friendlyautopep8
skip only deleted lines
autopep8 --in-place --line-range 23 38 ./friendlyautopep8/__init__.py
autopep8 --in-place --line-range 11 19 ./friendlyautopep8/__init__.py
```


```
$ friendlyautopep8 HEAD~13
autopep8 --in-place --line-range 12 78 ./friendlyautopep8/__init__.py
autopep8 --in-place --line-range 81 134 ./friendlyautopep8/__init__.py
```

### progrmatic:


```python
from friendlypep8 import run_on_cwd
run_on_cwd(commmitish_or_None):
```


## Why ?

Because autopep8 is nice but ["There must be a better
way"](https://www.youtube.com/watch?v=wf-BqAjZb8M). (Highly recommended to
watch). 

 
 - Applying autopep8 (or even fixing manually) can break tools like git blame. 
 - Extra changes (in whitespace, indent....) can distract reviewer from their tasks. 

The fix is simple, pep-8 (or should I say pycodestyle) only the lines that are
actively changed.

This will allow project that are not pep-8 complaint to __progressivley__
become compliant if they wish. And does not prevent you from running on your
changes.  

## TODO.

- Support applying on a commit range instead of non-comited
- Support non-git. 

## Limitations

Number of whitelines between function/classes might be wrong.  Probably other
things. 
