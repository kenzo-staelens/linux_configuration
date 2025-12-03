#!/usr/bin/python3
from argparse import ArgumentParser
from simple_term_menu import TerminalMenu
import os
import sys

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

parser = ArgumentParser(prog='Autocommit')
parser.add_argument('--many', help='Whether to commit many at once', action='store_true')

grp = parser.add_mutually_exclusive_group()
grp.add_argument('--mode', choices=MODES, help="long form mode parameter")
for mode in MODES:
    grp.add_argument(f'--{mode.lower()}', help=f'shorthand for --mode {mode}', action='store_true')

parser.add_argument('-m', '--message', help='message to use')
parser.add_argument('-b', '--base', help='base_commit')

parser.add_argument('--exclude', action='append', default=[], help="modules to exclude")
parser.add_argument('-p', '--push', help='git push the changes', action='store_true')
parser.add_argument('-f', '--force', help='enable force pushing', action='store_true')

args = parser.parse_args()

for mode in MODES: 
    if getattr(args, mode.lower()):
        args.mode = mode
        break

if not args.message and args.mode and (default_msg := DEFAULT_MESSAGES.get(args.mode)):
    args.message = default_msg


if args.many and not args.message:
    parser.error('Message is required when using many')

if args.base:
    os.system(f'git reset {args.base}')

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

def run_commit(module, message):
    os.system(f'git add {module}')
    os.system(f'git commit -m "{message}"')


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
    run_commit(module, constructed)

if args.push:
    push_args = ['git push']
    if args.force:
        push_args.append('--force-with-lease')
        push_args.append('--force-if-includes')
    cmd = ' '.join(push_args)
    os.system(cmd)
