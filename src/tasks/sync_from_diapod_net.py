#!/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import time

from src.utils import DBConnection, call_pod


class DiapodListParser(object):
    def __init__(self):
        self.retrieve_diapod_net_list()
        self.retrieve_known_pods_list()
        self.collect_pod_domains()

    def call_new_pods(self):
        for domain in self.pods:
            if not self.is_pod_known(domain):
                call_pod(domain)
                time.sleep(1)

    def retrieve_diapod_net_list(self):
        subprocess.call([
            "/usr/bin/wget",
            "https://diapod.net/active/public/dversions.test.txt",
            "-O",
            "/tmp/diapod_net_list.txt"
            ])

    def retrieve_known_pods_list(self):
        self.known_pods = []
        db = DBConnection()
        db.cursor.execute("select host from pods")
        rows = db.cursor.fetchall()
        for row in rows:
            self.known_pods.append(row["host"])
        db.close()

    def collect_pod_domains(self):
        list = []
        with open("/tmp/diapod_net_list.txt", "r") as f:
            for line in f:
                list.append(line.strip("\r\n"))
        self.pods = []
        for line in list:
            if line.find("Domain") > -1:
                self.pods.append(line.split(":")[1].strip())

    def is_pod_known(self, domain):
        if domain in self.known_pods:
            return True
        return False


if __name__ == '__main__':
    parser = DiapodListParser()
    parser.call_new_pods()
