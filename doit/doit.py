#!/usr/bin/env python

from concurrent.futures import ThreadPoolExecutor
import subprocess
import sys

f = sys.stdout


def execute_command(cmd, directory):
       p = subprocess.Popen(" ".join(cmd), shell=True, cwd=directory, stdout=subprocess.PIPE)
       return (directory, p.stdout.read().decode("utf-8"))


def do_in_parallell(cmd):
       def run_with_cmd(directory):
               return execute_command(cmd, directory)

       directories = [d.strip() for d in open("projects.txt").readlines()]
       with ThreadPoolExecutor(max_workers=len(directories)) as pool:
               for dir, result in pool.map(run_with_cmd, directories):
                       f.write(" ")
                       f.write(("%s " % dir).ljust(60, "-"))
                       f.write("\n")
                       f.write("\n")
                       f.write(result)
                       f.write("\n")
                       f.write("\n")


if __name__ == '__main__':
       import sys
       do_in_parallell(sys.argv[1:])
