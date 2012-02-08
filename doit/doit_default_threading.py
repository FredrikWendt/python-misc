#!/usr/bin/env python26
import threading
import Queue
import subprocess
import sys
import traceback

f = sys.stdout

QUIT_TOKEN = "QUIT_WORKER"

def worker (jobq, resultq):
    while True:
        arg = jobq.get(block=True)
        try:
            if arg == QUIT_TOKEN:
                break
            else:
                pos, cmd, directory = arg
                p = subprocess.Popen(" ".join(cmd), shell=True, cwd=directory, stdout=subprocess.PIPE)
                resultq.put( (pos, directory, p.stdout.read().decode("utf-8")) )
        except:
            traceback.print_exc()
        finally:
            jobq.task_done()
        
THREAD_COUNT = 5
def do_in_parallell(cmd):
    directories = [d.strip() for d in open("projects.txt").readlines()]
    # Create queues
    jobq = Queue.Queue()
    resultq = Queue.Queue()
    threads = []
    # Start a pool of workers
    for i in range(THREAD_COUNT):
        t = threading.Thread(target=worker, name='worker %i' % (i+1), args=(jobq, resultq))
        threads.append(t)
        t.start()

    # add jobs to do
    for pos, directory in enumerate(directories):
        jobq.put((pos, cmd, directory))

    # add a quit message at end of queue (one for every thread) 
    # ugly but we do not need timeouts and conditions
    for d in range(THREAD_COUNT):
        jobq.put(QUIT_TOKEN)
    
    results = []
    jobq.join()
    while True:
        try:
            results.append(resultq.get(block=False))
        except Queue.Empty:
            break

    for res in sorted(results):
        pos, directory, result = res     
        f.write(" ")
        f.write(("%s " % directory).ljust(60, "-"))
        f.write("\n")
        f.write("\n")
        f.write(result)
        f.write("\n")
        f.write("\n")

if __name__ == "__main__":
    command = sys.argv[1:]
    do_in_parallell(command)

