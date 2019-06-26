#!/usr/bin/env python3
import os, re, argparse

ProfileDir = os.path.expanduser("~/Library/MobileDevice/Provisioning Profiles")


def parse():
    parser = argparse.ArgumentParser(description="find and print profile suitable for a device")
    parser.add_argument('identifier', help='device identifier')
    return parser.parse_args()


def getContent(path):
    with open(path) as f:
        s = f.read()
    return s


ProFileNamePattern = re.compile(r'>Name<[^<]*<string>([^<]+)')


def print_profile(filePair):
    identifer, content = filePair
    m = ProFileNamePattern.search(content)
    if m: print(identifer, ":\t", m.group(1))
    else: print(identifer)


def main():
    args = parse()
    os.chdir(ProfileDir)
    profiles = [f for f in os.listdir('.') if f.endswith('.mobileprovision')]
    pros = [(f, getContent(f)) for f in profiles]
    pros = [f for f in pros if args.identifier in f[1]]
    for var in pros:
        print_profile(var)


if __name__ == '__main__':
    main()
