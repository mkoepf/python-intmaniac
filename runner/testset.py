#!/usr/bin/env python

from runner.testrun import Testrun
from tools import deep_merge
from threading import Thread

class Testset(Thread):

    def __init__(self, name='default', global_config={}):
        super().__init__()
        self.tests = []
        self.name = name
        self.global_config = global_config

    def set_global_config(self, global_config):
        self.global_config = global_config

    def add_from_config(self, name, config, global_config=None):
        global_config = global_config if global_config else self.global_config
        self.tests.append(Testrun(deep_merge(global_config, config),
                                  name="%s-%s" % (self.name, name)))

    def run(self):
        for test in self.tests:
            print(test)
        return 0


if __name__ == "__main__":
    print("Don't do this :)")
