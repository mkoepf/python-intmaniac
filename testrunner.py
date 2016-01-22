#!/usr/bin/env python

import yaml

from runner.testset import Testset

import sys
from argparse import ArgumentParser
import tools

test_config_stub = {'config': {}, 'meta': {}, 'environment': {}}
full_config_stub = {'global': test_config_stub, 'testsets': {}}
config = None
testconfig = None


def fail(errormessage):
    print("ERROR: %s" % errormessage)
    sys.exit(-10)


def get_test_set_groups():

    def get_setupdata():
        try:
            return \
                {**full_config_stub,
                 **yaml.safe_load(open(config.config_file, "r"))}
        except FileNotFoundError:
            fail("Could not find configuration file: %s" % config.config_file)

    def prepare_global_config(setupdata):
        global_config = setupdata['global']
        if config.env:
            for tmp in config.env:
                try:
                    k, v = tmp.split("=", 1)
                    global_config['environment'][k] = v
                except ValueError:
                    fail("Invalid environment setting: %s" % tmp)
        return global_config

    def get_test_sets_inner(setupdata):
        """Always returns a list of list of Testsets
            :param setupdata the full yaml setup data
        """
        test_set_groups = setupdata['testsets']
        global_config = setupdata['global']
        step = 0
        rv = []
        # if it's not a list, just wrap it into one.
        if type(test_set_groups) == dict:
            test_set_groups = [test_set_groups]
        for tsgroup in test_set_groups:
            tsgroup_list = []
            rv.append(tsgroup_list)
            # this must be dict now
            for tsname in sorted(tsgroup.keys()):
                # makes for predictable order for testing ...
                tests = tsgroup[tsname]
                tsname = "%02d-%s" % (step, tsname) \
                    if len(test_set_groups) > 1 \
                    else tsname
                tsglobal = tools.deep_merge(
                    global_config,
                    tests.pop("_global", test_config_stub))
                ts = Testset(name=tsname, global_config=tsglobal)
                tsgroup_list.append(ts)
                for test_name, test_config in tests.items():
                    ts.add_from_config(test_name, test_config)
            step += 1
        return rv

    setupdata = get_setupdata()
    prepare_global_config(setupdata)
    tmp = get_test_sets_inner(setupdata)
    return tmp


def run_test_set_groups(tsgs):
    retval = 0
    for testsetgroup in tsgs:
        for testset in testsetgroup:
            retval += testset.run()
    if not retval == 0:
        sys.exit(retval)


def prepare_environment(arguments):
    global config
    parser = ArgumentParser()
    parser.add_argument("-c", "--config-file",
                        help="specify configuration file",
                        default="./testrunner.yaml")
    parser.add_argument("-e", "--env",
                        help="dynamically add a value to the environment",
                        action="append")
    config = parser.parse_args(arguments)


if __name__ == "__main__":
    prepare_environment(sys.argv)
    run_test_set_groups(get_test_set_groups())
