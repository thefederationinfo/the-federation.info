#!/bin/env python
## Utils script to call a list of pods
import subprocess
import time
import sys


pods = open(sys.argv[1], 'r')
for pod in pods:
    print(pod.strip('\n\r'))
    subprocess.call('wget https://the-federation.info/register/'+pod.strip('\n\r')+' -O /dev/null', shell=True)
    time.sleep(1)
pods.close()
