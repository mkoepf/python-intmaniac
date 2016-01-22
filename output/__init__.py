#!/usr/bin/env python

output = None


class Output():
    @classmethod
    def set_output_type(cls, otype):
        global output
        if otype == "teamcity":
            output = TeamcityOutput()
        elif otype == "text":
            output = TextOutput()
        else:
            raise OutputException("Unknown Output type: %s" % otype)


class TextOutput():
    pass


class TeamcityOutput():
    pass


def init_output(otype):
    Output.set_output_type(otype)


if __name__ == "__main__":
    print("Don't do this :)")
