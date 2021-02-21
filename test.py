#!/usr/bin/env python3

import os, subprocess, tempfile

with tempfile.TemporaryDirectory(prefix="test", dir="/tmp") as tempdir:
    os.mkdir(tempdir+'/test')
    os.mkdir(tempdir+'/test/foo')
    os.mkdir(tempdir+'/test/foo/bar')
    os.mkdir(tempdir+'/test/foo/baz')
    os.mkdir(tempdir+'/test/foo/baz/quux')
    os.system('git init '+tempdir+'/test/foo/baz/git_workdir -b branchname --quiet')
    os.system('git init '+tempdir+'/test/foo/baz/git_workdir_empty -b branchname --quiet')
    os.system('git init --bare '+tempdir+'/test/foo/baz/git_bare -b branchname --quiet')
    os.system('git init --bare '+tempdir+'/test/foo/baz/git_bare_empty -b branchname --quiet')
    os.system('cd '+tempdir+'/test/foo/baz/git_workdir && echo a > toto')
    os.system('cd '+tempdir+'/test/foo/baz/git_workdir && git add toto')
    os.system('cd '+tempdir+'/test/foo/baz/git_workdir&& GIT_COMMITTER_DATE="Sun Feb 21 18:00 2020 +0000" GIT_AUTHOR_NAME="Suzanne Soy" GIT_AUTHOR_EMAIL="example@suzanne.soy" GIT_COMMITTER_NAME="Suzanne Soy" GIT_COMMITTER_EMAIL="example@suzanne.soy" git commit -m "example commit for tests" --date="Sun Feb 21 18:00 2020 +0000" --quiet')
    os.system('cd '+tempdir+'/test/foo/baz/git_workdir && git push ../git_bare branchname --quiet')
    # It seems that sqlite databases are quite reproducible; running the same command produces identical files!
    os.system('sqlite3 '+tempdir+'/test/foo/baz/db "create table digits(d);"')
    for i in range(10):
      os.system('sqlite3 '+tempdir+'/test/foo/baz/db "insert into digits(d) values('+str(i)+');"')
    os.system('sqlite3 '+tempdir+'/test/foo/baz/db "create table tbl(x);"')
    os.system('sqlite3 '+tempdir+'/test/foo/baz/db "insert into tbl(x) select d0.d * 1000000 + d1.d * 100000 + d2.d * 10000 + d3.d * 1000 + d4.d * 100 + d5.d * 10 + d6.d from digits d0, digits d1, digits d2, digits d3, digits d4, digits d5, digits d6;"')
    os.system('sqlite3 '+tempdir+'/test/foo/baz/db "create table rnd(x);"')
    os.system('sqlite3 '+tempdir+'/test/foo/baz/db "insert into rnd(x) select x from tbl order by random();"')
    os.system('sqlite3 '+tempdir+'/test/foo/baz/db "create table tbl2(x);"')
    os.system('sqlite3 '+tempdir+'/test/foo/baz/db "insert into tbl2(x) select x from rnd order by x;"')
    os.system('sqlite3 '+tempdir+'/test/foo/baz/db "drop table rnd;"')
    #os.system('sqlite3 '+tempdir+'/test/foo/baz/db "vacuum;"')
    os.system('echo a > '+tempdir+'/test/foo/baz/titi')
    os.system('cp -ai '+tempdir+' /tmp/xxx')
    h = subprocess.check_output([os.path.abspath('./hash-files.py'), 'test/foo'], cwd=tempdir).strip()
    if h == b'e8e0e538fa2a79a6c03d5575734bb77ee8c8734b07201d3d7dfc289c118d81a4':
        print("test passed")
    else:
        print("TEST FAILED: got hash " + repr(h))
        exit(1)