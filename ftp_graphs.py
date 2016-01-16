#!/usr/bin/python
import paramiko
import os
from commands import getstatusoutput
from config import config

DIR = os.path.dirname(os.path.realpath(__file__))

if os.path.isfile(os.path.join(DIR, 'temp.rrd')):
    getstatusoutput(os.path.join(DIR, 'get_temp.py'))

if os.path.isfile(os.path.join(DIR, 'humidity.rrd')):
    getstatusoutput(os.path.join(DIR, 'get_humidity.pl'))

getstatusoutput(os.path.join(DIR, 'create_graphs.py'))

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(config['remote']['host'], username=config['remote']['user'])

sftp = ssh.open_sftp();
for root, dirs, files in os.walk(os.path.join(DIR, 'latest_graphs')):
    for name in files:
        local_path = os.path.join(root, name)
        remote_folder = os.path.join(config['remote']['path'], 'latest_graphs')
        remote_path = os.path.join(remote_folder, name)
        sftp.put(local_path, remote_path)

sftp.close()
