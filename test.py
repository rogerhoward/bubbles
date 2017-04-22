#!/usr/bin/env python
import os, sys
import config
import utils
from pprint import pprint
import boto3
#------------------------------------------------#
#  Command line options                          #
#------------------------------------------------#

def main():
    pass

if __name__ == '__main__':
    p = utils.get_galleries()

    pprint(p)

    [pprint(utils.get_panos_for(x)) for x in p]