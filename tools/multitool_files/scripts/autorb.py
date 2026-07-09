import re
from argparse import Namespace
from typing import Any
import os

PATTERN = r'<{7} HEAD\n## (\d{2}(?:\.\d+){4})(.*)={7}\n## (\d{2}(?:\.\d+){4})(.*)?\n>{7}.*?\n\n## (\d{2}(?:\.\d+){4})'

BASE_PATH = '{}/{}'

def run(args: Namespace, ctx: dict[str, Any]):
    target_v = None
    newfile = None
    path = BASE_PATH.format(args.target, 'CHANGELOG.md')
    with open(path, 'r+') as f:
        read = f.read()
        newfile = read
        res = re.findall(PATTERN, read, re.DOTALL)
        if res:
            res = res[0]
            incoming_v = res[0].split('.')
            my_v = res[2].split('.')
            old_v = res[4].split('.')
            target_v = incoming_v.copy()

            if not any(a>b for a,b in zip(my_v, incoming_v)):
                # find node where old and current change differ
                for i in range(5):
                    if my_v[i] > old_v[i]:
                        break
                    
                for j in range(i, 5):
                    if j==i:
                        target_v[j] = str(int(target_v[j])+1)
                    else:
                        target_v[j] = '0'
            else:
                target_v = my_v
            target_v = '.'.join(target_v)
            incoming = '## ' + '.'.join(incoming_v) + res[1]
            ours = '## ' + target_v + res[3]
            newfile = re.sub(r'<{7}.*?>{7}.*?\n', ours + '\n\n' + incoming , read, flags=re.DOTALL)
            if newfile:
                f.seek(0)
                f.write(newfile)
                f.truncate()

    if target_v:
        path = BASE_PATH.format(args.target, '__manifest__.py')
        with open(path, 'r+') as f:
            read = f.read()
            if re.match(r'<{7}.*>{7}', read, re.DOTALL):
                res = re.sub(r'<{7}.*>{7}', f"    'version': '{target_v}'," , read, flags=re.DOTALL)
            else:
                print('e', target_v)
                res = re.sub(r"'version':.*", f"'version': '{target_v}',", read)
            if res:
                f.seek(0)
                f.write(res)
                f.truncate()
    
    os.system('git add .')
    os.system('git -c core.editor=true rebase --continue')
    