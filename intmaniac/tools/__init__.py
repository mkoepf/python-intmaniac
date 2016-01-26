#!/usr/bin/env python


# python 3.5 only
def deep_merge(d0, d1):
    d = {**d0, **d1}
    for k, v in d1.items():
        if type(v) == dict and k in d0 and type(d0[k]) == dict:
            d1[k] = deep_merge(d0[k], v)
    for k, v in d0.items():
        if not k in d1:
            d1[k] = v
    return d


if __name__ == "__main__":
    print("Don't do this :)")