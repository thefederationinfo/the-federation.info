#!/bin/env python
## Utils script to call a list of pods

import subprocess

pods = open('/tmp/pods.txt', 'r')
for pod in pods:
    print pod.strip('\n\r')
    subprocess.call('wget http://pods.jasonrobinson.me/register/'+pod.strip('\n\r')+' -O /dev/null', shell=True)
    

