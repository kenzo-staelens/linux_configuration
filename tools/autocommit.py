#!/usr/bin/python3
#PYTHON_ARGCOMPLETE_OK
from argparse import ArgumentParser, RawTextHelpFormatter
import argcomplete
from simple_term_menu import TerminalMenu
import os
import sys
import re

MODES = [
    'DEV',
    'ADD',
    'FIX',
    'MIG',
    'DEL',
    'ADM',
    'WIP',
]

DEFAULT_MESSAGES = {
    'ADD': 'Module created',
    'MIG': 'Migrate module',
    'DEL': 'Module removed',
    'WIP': '',
}

parser = ArgumentParser(prog='Autocommit', formatter_class=RawTextHelpFormatter)
parser.add_argument('--many', help='Whether to add multiple modules to a single commit', action='store_true')

grp = parser.add_mutually_exclusive_group()
grp.add_argument(
    '--mode',
    choices=MODES,
    help="long form mode parameter\n"
    + "creates selection menu if omitted\n"
    + '\n'.join([
        f'  - defaults to "{m}" if {mode} selected'
        for mode,m in DEFAULT_MESSAGES.items()
    ])
)
for mode in MODES:
    grp.add_argument(f'--{mode.lower()}', help=f'shorthand for --mode {mode}', action='store_true')

parser.add_argument('-m', '--message', help='message to use, asked per module if omitted')
mutex_base_grp = parser.add_mutually_exclusive_group()
mutex_base_grp.add_argument('-b', '--base', help='reset to this commit hash and recommits those modules')
mutex_base_grp.add_argument('--based', help='reset to <n> commits back and recommit those modules')

# parser.add_argument('-b', '--base', help='reset to this commit hash and recommits those modules')

parser.add_argument('--exclude', action='append', default=[], help="modules to exclude")
parser.add_argument('-p', '--push', help='git push the changes', action='store_true')
parser.add_argument('-f', '--force', help='enable force pushing', action='store_true')
parser.add_argument('-s', '--setup', help='setup a non existing branch', action='store_true')
parser.add_argument('-n', '--no-hooks', help='adds \'-n\' to commits', action='store_true')

argcomplete.autocomplete(parser)

args = parser.parse_args()

for mode in MODES:
    if getattr(args, mode.lower()):
        args.mode = mode
        break

if not args.message and args.mode and (default_msg := DEFAULT_MESSAGES.get(args.mode)):
    args.message = default_msg


if args.many and not args.message:
    parser.error('Message is required when using many')

def parse(target, n_commits):
    head = os.popen('git log --oneline').read()
    pattern = r'(.{7})(?: \(.*\))? \[(\w{3})\] (\w+) - (.*)'
    matched = []
    for i, x in enumerate(head.split('\n')):
        m = re.match(pattern, x)
        match_hash = re.match('^(.{7}).*', x)
        if (match_hash and match_hash.group(1) == target) or i == n_commits:
            break
        if not m:
            continue    
        if m.group(1)== target or i == n_commits:
            break
        matched.append(m.groups())
    return matched

matched = []
if args.base:
    matched = parse(args.base, None)
    os.system(f'git reset {args.base}')

if args.based:
    matched = parse(None, int(args.based))
    os.system(f'git reset HEAD~{args.based}')


def get_mode(args, extra_title=None):
    mode = args.mode

    title = 'Commit type'
    if extra_title:
        title += f' ({extra_title})'
    title += ':'

    if not mode:
        terminal_menu = TerminalMenu(
            MODES,
            title=title,
        )
        idx = terminal_menu.show()
        mode = MODES[idx]
        print(mode)
    return mode

def get_message(args, module, mode):
    if args.message:
        message = args.message
    else:
        message = input(f'commit_message {module}:\n')
    if not message or message.strip() == '':
        message = DEFAULT_MESSAGES.get(mode, '')
    if not message:
        print('\x1b[31m\x1b[1mNo message selected\x1b[0m')
        sys.exit()
    return message

def get_modules(args):
    cmd = "git status --porcelain | awk -F'/' '{ print $1 }' | awk '{ print $2 }' | uniq"
    res = os.popen(cmd).read()
    files = res.split('\n')[:-1] # remove empty strings
    files = [file for file in files if file not in args.exclude]
    return files

def run_commit(args, module, message):
    os.system(f'git add {module}')
    commit = f'git commit -m "{message}"' 
    if args.no_hooks:
        commit+= ' -n'
    os.system(commit)

def get_git_branch():
    return os.popen('git rev-parse --abbrev-ref HEAD').read().strip()

# reconstruct from old commits
for _, mode, module, message in matched:
    constructed = f'[{mode}] {module} - {message}'
    run_commit(args, module, constructed)

modules = get_modules(args)

if args.many:
    mode = get_mode(args)

for module in modules:
    if (not args.many):
        mode = get_mode(args, module)
    if args.mode != 'WIP':
        message = get_message(args, module, mode).capitalize()
        constructed = f'[{mode}] {module} - {message}'
    else:
        constructed = '[WIP]'
    run_commit(args, module, constructed)

if args.push:
    push_args = ['git push']
    if args.force:
        push_args.append('--force-with-lease')
        push_args.append('--force-if-includes')
    if args.setup:
        push_args.append('--set-upstream')
        push_args.append('origin')
        push_args.append(get_git_branch())
    cmd = ' '.join(push_args)
    os.system(cmd)
