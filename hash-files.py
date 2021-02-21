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

def hashN(bytesList):
  #print("hashN ")
  #print(b''.join(bytesList))
  return subprocess.check_output(['sha256sum', '--binary', '--zero'], input = b''.join(bytesList))[0:64]

#
# TODO: use this to get the hashes and names for all roots of the DAG (commits that are reachable only through one (or several) direct branch names, but not transitively as ancestors of other commits)
#
git_command='''
  (
    (
      git log --format=%P --all HEAD FETCH_HEAD | tr ' ' \\n | grep -v '^$' | sort -u | sed -e 'p;p';
      git rev-parse HEAD FETCH_HEAD --all | sort -u
    ) | sort | uniq -u;
    for ref in HEAD FETCH_HEAD; do echo "$(git rev-parse $ref) $ref"; done; git for-each-ref --format='%(objectname) %(refname)'
  ) | sort | awk 'BEGIN { h="" } { if (length($0) == 40) { h=$0 } else { if (substr($0,1,40) == h) print $0 } }' | sort -k 2
'''

def hashGit(path):
  return subprocess.check_output(['sh', '-c', git_command])

sqlite3_command='''
  (
    sqlite3 file.db .dump | sort | sha256sum --binary --zero
  )
'''

def hashSqlite3(path):
  pass # TODO…

def recur(x):
  #print(x)
  # initial list of paths
  if isinstance(x, list):
    return hashN([b'root\0'] + [recur(os.path.abspath(path)) + b'  ' + path.encode('utf-8') + b'\0' for path in sorted(x)])
  # GIT repo
  elif os.path.isdir(x) and os.path.exists(os.path.join(x, '.git')):
    print("GIT DIR")
    return hashN([b'git-versioned folder\0', hashGit(x)])
  # directory
  elif os.path.isdir(x):
   return hashN([b'directory\0'] + [recur(entry) + b'  ' + entry.encode('utf-8') + b'\0' for entry in os.listdir(x)])
  # Just a file
  elif os.path.isfile(x):
    return hashFile(x)
  else:
    sys.exit("unknown file type for %s" % f)

print(recur(sys.argv[1:]).decode('utf-8'))
