#!/usr/bin/env python3

import os, subprocess, tempfile

# Empty
with tempfile.TemporaryDirectory(prefix="test", dir="/tmp") as tempdir:
    os.mkdir(tempdir+'/test')
    os.mkdir(tempdir+'/test/foo')
    h = subprocess.check_output([os.path.abspath('./hash-files.py'), 'test/foo'], cwd=tempdir).strip()
    if h == b'dc99f8161ccf245e178102a00264e4f4f43cd0048ea525b6c9e226777414352f':
        print("test passed: empty")
    else:
        print("TEST FAILED: empty: got hash " + repr(h))
        exit(1)

# Plain text file
with tempfile.TemporaryDirectory(prefix="test", dir="/tmp") as tempdir:
    os.mkdir(tempdir+'/test')
    os.mkdir(tempdir+'/test/foo')
    os.system('echo a > '+tempdir+'/test/foo/x')
    h = subprocess.check_output([os.path.abspath('./hash-files.py'), 'test/foo'], cwd=tempdir).strip()
    if h == b'6b393b2233479ccc54975f83f4de0d39592d5ab78cd02b19597e7bbe97f43cf1':
        print("test passed: plain text file")
    else:
        print("TEST FAILED: plain text file: got hash " + repr(h))
        exit(1)

# Plain text file and empty folder in subdirectory
with tempfile.TemporaryDirectory(prefix="test", dir="/tmp") as tempdir:
    os.mkdir(tempdir+'/test')
    os.mkdir(tempdir+'/test/foo')
    os.mkdir(tempdir+'/test/foo/bar')
    os.mkdir(tempdir+'/test/foo/baz')
    os.mkdir(tempdir+'/test/foo/baz/quux')
    os.system('echo a > '+tempdir+'/test/foo/baz/titi')
    h = subprocess.check_output([os.path.abspath('./hash-files.py'), 'test/foo'], cwd=tempdir).strip()
    if h == b'7421373b28f6a1929228a3bd7ecb23123d25da36c9bbe41518c7a6252f351712':
        print("test passed: plain text and empty folder in subdirectory")
    else:
        print("TEST FAILED: plain text and empty folder in subdirectory: got hash " + repr(h))
        exit(1)

# Git directories
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
    os.system('echo a > '+tempdir+'/test/foo/baz/titi')
    h = subprocess.check_output([os.path.abspath('./hash-files.py'), 'test/foo'], cwd=tempdir).strip()
    if h == b'8a84206ece36f07d2c408e565ec506bab407d6e1c645eb4a5c7d057049956110':
        print("test passed: git")
        subprocess.check_output("tar -zcf /tmp/debug-git.tar.gz .", cwd=tempdir, shell=True)
    else:
        print("TEST FAILED: git: got hash " + repr(h))
        subprocess.check_output("tar -zcf /tmp/debug-git.tar.gz .", cwd=tempdir, shell=True)
        exit(0)

# Sqlite
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
    os.system('sqlite3 '+tempdir+'/test/foo/baz/db "insert into tbl(x) select d4.d * 100 + d5.d * 10 + d6.d from digits d4, digits d5, digits d6;"')
    os.system('sqlite3 '+tempdir+'/test/foo/baz/db "create table rnd(x);"')
    os.system('sqlite3 '+tempdir+'/test/foo/baz/db "insert into rnd(x) select x from tbl order by random();"')
    os.system('sqlite3 '+tempdir+'/test/foo/baz/db "create table tbl2(x);"')
    os.system('sqlite3 '+tempdir+'/test/foo/baz/db "insert into tbl2(x) select x from rnd order by x;"')
    os.system('sqlite3 '+tempdir+'/test/foo/baz/db "drop table rnd;"')
    #os.system('sqlite3 '+tempdir+'/test/foo/baz/db "vacuum;"')
    os.system('echo a > '+tempdir+'/test/foo/baz/titi')
    h = subprocess.check_output([os.path.abspath('./hash-files.py'), 'test/foo'], cwd=tempdir).strip()
    if h == b'c04f602dcb7eec19433c12981f58d653c61ac7453da60e375f2f5587dc57f474':
        print("test passed: sqlite")
        subprocess.check_output("tar -zcf /tmp/debug-sql.tar.gz .", cwd=tempdir, shell=True)
    else:
        print("TEST FAILED: sqlite got hash " + repr(h))
        subprocess.check_output("tar -zcf /tmp/debug-sql.tar.gz .", cwd=tempdir, shell=True)
        exit(0)

# Sqlite big table
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
    h = subprocess.check_output([os.path.abspath('./hash-files.py'), 'test/foo'], cwd=tempdir).strip()
    if h == b'b0aae011d0e438a78d6e2652478ec667b7650b9c29dc6d7235ccce26a75c95cb':
        print("test passed: sqlite big table")
        subprocess.check_output("tar -zcf /tmp/debug-sql.tar.gz .", cwd=tempdir, shell=True)
    else:
        print("TEST FAILED: sqlite big table got hash " + repr(h))
        subprocess.check_output("tar -zcf /tmp/debug-sql.tar.gz .", cwd=tempdir, shell=True)
        exit(0)