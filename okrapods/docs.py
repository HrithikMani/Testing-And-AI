#!/usr/bin/env python
import os
import re
import jinja2

def parsePod(src):
    docstring = 'No docstring found'
    description = ''
    elements = []
    verbs = []
    m = re.search('"""(.*?)"""', src, re.DOTALL)
    if m:
        docstring = m.group(1).strip()
        description = docstring.split('\n')[0].strip()
        src = src[m.end():]
    for m in re.findall('^$\n^@(\w+)$(.*?)\n^$', src, re.DOTALL|re.MULTILINE):
        verbs.append({
            'name': m[0],
            'definition': m[1]
        })
    for m in re.findall('^$\n^([-+*\d]+:)?(\w+):(.*?)^$', src, re.DOTALL|re.MULTILINE):
        elements.append({
            'name': m[1],
            'timeout': m[0][:-1] if m[0] else None,
            'definition': m[2],
        })
    return {
        'docstring': docstring,
        'description': description,
        'elements': elements,
        'verbs': verbs
    }

def main():
    thisDir = os.path.dirname(os.path.abspath(__file__))
    outDir = os.path.join(thisDir, 'docs')
    pods = {}
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    with open(os.path.join(thisDir, 'index.html')) as fp:
        it = jinja2.Template(fp.read(), autoescape=True)
    with open(os.path.join(thisDir, 'pod.html')) as fp:
        pt = jinja2.Template(fp.read(), autoescape=True)
    for f in os.listdir(os.path.join(thisDir, 'webchart')):
        if f.endswith('.pod'):
            title = os.path.splitext(f)[0]
            with open(os.path.join(thisDir, 'webchart', f)) as fp:
                data = parsePod(fp.read())
                pods[title] = data
                pods[title]['title'] = title
            if pods.get(title):
                with open(os.path.join(outDir, '{0}.html'.format(title)), 'w') as fp:
                    fp.write(pt.render(pod=pods.get(title)))
    with open(os.path.join(outDir, 'index.html'), 'w') as fp:
        fp.write(it.render(pods=pods))    

if __name__ == '__main__':
    main()
