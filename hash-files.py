#!/usr/bin/env python3

import os
import sys
import subprocess

def debug(s):
  #print(s, file=sys.stderr, flush=True)
  pass


def hashFile(filename):
  result = subprocess.check_output(['sha256sum', '--binary', '--zero', filename])[0:64]
  debug("hashFile("+filename+") = "+str(result))
  return result

def hash1(bytes_):
  result = subprocess.check_output(['sha256sum', '--binary', '--zero'], input=bytes_)[0:64]
  debug("hash1("+str(bytes_)+") = "+str(result))
  return result

#
# TODO: use this to get the hashes and names for all roots of the DAG (commits that are reachable only through one (or several) direct branch names, but not transitively as ancestors of other commits)
#
git_command='''
  (
    (
      git log --format=%P --all {HEAD} {FETCH_HEAD} | tr ' ' \\n | grep -v '^$' | LC_ALL=C sort -u | sed -e 'p;p';
      git rev-parse {HEAD} {FETCH_HEAD} --all | LC_ALL=C sort -u
    ) | LC_ALL=C sort | uniq -u;
    for ref in {HEAD} {FETCH_HEAD}; do echo "$(git rev-parse $ref) $ref"; done; git for-each-ref --format='%(objectname) %(refname)'
  ) | LC_ALL=C sort \
    | awk 'BEGIN {{ h="" }} {{ if (length($0) == 40) {{ h=$0 }} else {{ if (substr($0,1,40) == h) print $0 }} }}' \
    | LC_ALL=C sort -k 2
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
  result = subprocess.check_output(['sh', '-c', git_command.format(HEAD=HEAD, FETCH_HEAD=FETCH_HEAD)], cwd=path)
  debug("hashGit("+path+") = "+str(result))
  return result

def hashSqlite3(path):
  result= subprocess.check_output(['sh', '-c', 'sqlite3 "$1" .dump | LC_ALL=C sort | sha256sum --binary --zero', '--', os.path.abspath(path)])
  debug("hashSqlite3("+path+") = "+str(result))
  return result

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

def recur(depth, x):
  # initial list of paths
  if isinstance(x, list):
    debug("ROOT " + str(depth) + ' [' + ', '.join(x) + ']')
    return b'root\0' + b''.join(recur(depth + 1, os.path.abspath(path)) + b'  ' + path.encode('utf-8') + b'\0' for path in sorted(x))
  # GIT repo
  elif is_git(x):
    debug("GIT DIR " + str(depth) + ' ' + x)
    return hash1(b'git-versioned folder\0' + hashGit(x))
  # directory
  elif os.path.isdir(x):
    debug("DIR " + str(depth) + ' ' + x)
    return hash1(b'directory\0' + b''.join(recur(depth + 1, os.path.join(x, entry)) + b'  ' + entry.encode('utf-8') + b'\0' for entry in sorted(os.listdir(x))))
  elif b'SQLite 3.x database' in subprocess.check_output(["file", x]):
    debug("SQLITE3 " + str(depth) + ' ' + x)
    return hashSqlite3(x)
  # Just a file
  elif os.path.isfile(x):
    debug("PLAIN FILE " + str(depth) + ' ' + x)
    return hashFile(x)
  else:
    sys.exit("unknown file type for %s" % os.path.abspath(x))

print(hash1(recur(0, sys.argv[1:])).decode('utf-8'), flush=True)
