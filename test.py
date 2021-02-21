#!/usr/bin/env python3

import os, subprocess, tempfile

with tempfile.TemporaryDirectory(prefix="test", dir="/tmp") as tempdir:
    os.mkdir(tempdir+'/test')
    os.mkdir(tempdir+'/test/foo')
    os.mkdir(tempdir+'/test/foo/bar')
    os.mkdir(tempdir+'/test/foo/baz')
    os.mkdir(tempdir+'/test/foo/baz/quux')
    os.system('git init '+tempdir+'/test/foo/baz/git_workdir -b branchname')
    os.system('git init '+tempdir+'/test/foo/baz/git_workdir_empty -b branchname')
    os.system('git init --bare '+tempdir+'/test/foo/baz/git_bare -b branchname')
    os.system('git init --bare '+tempdir+'/test/foo/baz/git_bare_empty -b branchname')
    os.system('cd '+tempdir+'/test/foo/baz/git_workdir && echo a > toto')
    os.system('cd '+tempdir+'/test/foo/baz/git_workdir && git add toto')
    os.system('cd '+tempdir+'/test/foo/baz/git_workdir&& GIT_COMMITTER_DATE="Sun Feb 21 18:00 2020 +0000" GIT_AUTHOR_NAME="Suzanne Soy" GIT_AUTHOR_EMAIL="example@suzanne.soy" GIT_COMMITTER_NAME="Suzanne Soy" GIT_COMMITTER_EMAIL="example@suzanne.soy" git commit -m "example commit for tests" --date="Sun Feb 21 18:00 2020 +0000"')
    os.system('cd '+tempdir+'/test/foo/baz/git_workdir && git push ../git_bare branchname')
    #os.system('sqlite3 '+tempdir+'/test/foo/baz/db "create table tbl(x)"')
    os.system('echo a > '+tempdir+'/test/foo/baz/titi')
    os.system('cp -ai '+tempdir+' /tmp/xxx')
    print('')
    h = subprocess.check_output([os.path.abspath('./hash-files.py'), 'test/foo'], cwd=tempdir).strip()
    if h == b'8a84206ece36f07d2c408e565ec506bab407d6e1c645eb4a5c7d057049956110':
        print("test passed")
    else:
        print("TEST FAILED: got hash " + repr(h))
        exit(1)