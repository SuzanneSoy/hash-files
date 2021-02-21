#!/usr/bin/env python3

import os
import sys
import subprocess

def hashFile(filename):
  #print("hashFile " + filename)
  return subprocess.check_output(['sha256sum', '--binary', '--zero', filename])[0:64]

def hash1(bytes):
  #print("hash1 " + bytes)
  return subprocess.check_output(['sha256sum', '--binary', '--zero'], input=bytes)[0:64]

#
# TODO: use this to get the hashes and names for all roots of the DAG (commits that are reachable only through one (or several) direct branch names, but not transitively as ancestors of other commits)
#
git_command='''
  (
    (
      git log --format=%P --all {HEAD} {FETCH_HEAD} | tr ' ' \\n | grep -v '^$' | sort -u | sed -e 'p;p';
      git rev-parse {HEAD} {FETCH_HEAD} --all | sort -u
    ) | sort | uniq -u;
    for ref in {HEAD} {FETCH_HEAD}; do echo "$(git rev-parse $ref) $ref"; done; git for-each-ref --format='%(objectname) %(refname)'
  ) | sort | awk 'BEGIN {{ h="" }} {{ if (length($0) == 40) {{ h=$0 }} else {{ if (substr($0,1,40) == h) print $0 }} }}' | sort -k 2
'''

def ref_exists(path, ref):
  try:
    subprocess.check_output("git rev-parse --verify "+ref+" 2>/dev/null", cwd=path, shell=True)
    return True
  except subprocess.CalledProcessError:
    return False

def hashGit(path):
  FETCH_HEAD = "FETCH_HEAD" if ref_exists(path, "FETCH_HEAD") else ''
  HEAD       =       "HEAD" if ref_exists(path,       "HEAD") else ''
  return subprocess.check_output(['sh', '-c', git_command.format(HEAD=HEAD, FETCH_HEAD=FETCH_HEAD)], cwd=path)

def hashSqlite3(path):
  return subprocess.check_output(['sh', '-c', 'sqlite3 "$1" .dump | sort | sha256sum --binary --zero', '--', os.path.abspath(path)])

def ignore_exitcode(cmd, **kwargs):
  try:
     return subprocess.check_output(cmd, **kwargs)
  except subprocess.CalledProcessError:
    return ''

def is_git(x):
  return os.path.isdir(x) \
         and (ignore_exitcode("git rev-parse --is-inside-git-dir 2>/dev/null",   cwd=x, shell=True).strip() == b'true' or
              ignore_exitcode("git rev-parse --is-inside-work-tree 2>/dev/null", cwd=x, shell=True).strip() == b'true')
         # TODO: if a file which is inside a larger git dir is passed on the CLI, this still returns True :-(

def recur(x):
  #print(x)
  # initial list of paths
  if isinstance(x, list):
    return b'root\0' + b''.join(recur(os.path.abspath(path)) + b'  ' + path.encode('utf-8') + b'\0' for path in sorted(x))
  # GIT repo
  elif is_git(x):
    #print("GIT DIR " + x, file=sys.stderr)
    return hash1(b'git-versioned folder\0' + hashGit(x))
  # directory
  elif os.path.isdir(x):
    return hash1(b'directory\0' + b''.join(recur(os.path.join(x, entry)) + b'  ' + entry.encode('utf-8') + b'\0' for entry in os.listdir(x)))
  elif b'SQLite 3.x database' in subprocess.check_output(["file", x]):
    return hashSqlite3(x)
  # Just a file
  elif os.path.isfile(x):
    return hashFile(x)
  else:
    sys.exit("unknown file type for %s" % os.path.abspath(x))

print(hash1(recur(sys.argv[1:])).decode('utf-8'))
