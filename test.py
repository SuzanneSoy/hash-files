#!/usr/bin/env python3

import os, subprocess, tempfile

# Empty
with tempfile.TemporaryDirectory(prefix="test", dir="/tmp") as tempdir:
    os.mkdir(tempdir+'/test')
    os.mkdir(tempdir+'/test/foo')
    h = subprocess.check_output([os.path.abspath('./hash-files.py'), 'test/foo'], cwd=tempdir).strip()
    if h == b'dc99f8161ccf245e178102a00264e4f4f43cd0048ea525b6c9e226777414352f':
        print("test passed: empty\n", flush=True)
    else:
        print("TEST FAILED: empty: got hash " + repr(h) + "\n", flush=True)
        exit(1)

# Plain text file
with tempfile.TemporaryDirectory(prefix="test", dir="/tmp") as tempdir:
    os.mkdir(tempdir+'/test')
    os.mkdir(tempdir+'/test/foo')
    os.system('echo a > '+tempdir+'/test/foo/x')
    h = subprocess.check_output([os.path.abspath('./hash-files.py'), 'test/foo'], cwd=tempdir).strip()
    if h == b'6b393b2233479ccc54975f83f4de0d39592d5ab78cd02b19597e7bbe97f43cf1':
        print("test passed: plain text file\n", flush=True)
    else:
        print("TEST FAILED: plain text file: got hash " + repr(h) + "\n", flush=True)
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
    if h == b'0bb2f31bf05eb215ebef32abcc62cddbfad2d8b0a1221bb335da0acaf3455558':
        print("test passed: plain text and empty folder in subdirectory\n", flush=True)
    else:
        print("TEST FAILED: plain text and empty folder in subdirectory: got hash " + repr(h) + "\n", flush=True)
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
    if h == b'f31eb7e1bcb25e79be0d1305d58eeadbe3fd9bf38ecbd0449789e8c91b5f4340':
        print("test passed: git\n", flush=True)
        subprocess.check_output("tar -zcf /tmp/debug-git.tar.gz .", cwd=tempdir, shell=True)
    else:
        print("TEST FAILED: git: got hash " + repr(h) + "\n", flush=True)
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
    if h == b'b775b5c3ad1b403c08fa88e43be42bd76143f93c26bf42cb8881c595161a5509':
        print("test passed: sqlite\n", flush=True)
        subprocess.check_output("tar -zcf /tmp/debug-sql.tar.gz .", cwd=tempdir, shell=True)
    else:
        print("TEST FAILED: sqlite got hash " + repr(h) + "\n", flush=True)
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
    if h == b'7d6917fef222456552b6359ddc4eee235a0cdca089c0a6d9b4b2f6a747987eb9':
        print("test passed: sqlite big table\n", flush=True)
        subprocess.check_output("tar -zcf /tmp/debug-sql.tar.gz .", cwd=tempdir, shell=True)
    else:
        print("TEST FAILED: sqlite big table got hash " + repr(h) + "\n", flush=True)
        subprocess.check_output("tar -zcf /tmp/debug-sql.tar.gz .", cwd=tempdir, shell=True)
        exit(0)