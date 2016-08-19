#!/usr/bin/env python
# encoding: utf-8

import os, re, argparse, subprocess
from Cheetah.Template import Template

template_path = "/Users/mac/bin/data/xcode-makefile.tmpl"

def parse():
    parser = argparse.ArgumentParser(
            description = 'generate Makefile from xcode project')
    parser.add_argument('project_path', nargs = '?',
            help='path to the project, default find in cur work dir')
    parser.add_argument('-o', '--output',
            help='output filename, default is `Makefile`', default='Makefile')
    return parser.parse_args()

def getSectionData(sectionName, source):
    pat = re.compile(r'^(\s*)%s:\s*$((?:\s*^\1\s+\S.*$)+)'%sectionName,
            re.MULTILINE)
    match = pat.search(source)
    if match.group(2):
        return [s for s in
                re.findall(r'^\s*(\S.*)$', match.group(2), re.MULTILINE)]
    return None

def getProjectInfo(project_path):
    p = subprocess.Popen(["xcodebuild", "-list", "-project", "%s"%project_path],
            stdout = subprocess.PIPE)
    out,_ = p.communicate()
    if p.returncode != 0:
        return None
    configurations = getSectionData("Build Configurations", out)
    schemes = getSectionData("Schemes", out)
    return {'configurations':configurations, 'schemes':schemes}

def renderTemplate(info):
    return Template(file=template_path, searchList=info)

def main():
    args = parse()
    if not args.project_path:
        files = [f for f in os.listdir('.') if f.endswith('.xcodeproj')]
        if not files:
            print('please set project_path!!')
            return
        args.project_path = files[0]
    info = getProjectInfo(args.project_path)
    if not info: print('error occur'); return
    info['project_path'] = args.project_path
    out = str(renderTemplate(info))
    with open(args.output, 'w') as f:
        f.write(out)
    print('output to %s'%(args.output))

if __name__ == '__main__':
    main()
