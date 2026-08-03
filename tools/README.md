# Custom tooling

## Autocommit

More or less feature complete single-file tool to automatically commit multiple odoo modules compliant with Accomodata git guidelines

- 1 module per commit
- prefixed with the type of commit [DEV|ADD|FIX|MIG|DEL|ADM|WIP]
- format `[PREFIX] module_name - message`

|argument|use|mutexgroup|
|---|---|---|
|--mode|long form for defining module commit prefix|prefix|
|--dev|commits all modules with [DEV] prefix|prefix|
|--add|commits all modules with [ADD] prefix (default message exists)|prefix|
|--fix|commits all modules with [FIX] prefix|prefix|
|--mig|commits all modules with [MIG] prefix (default message exists)|prefix|
|--del|commits all modules with [DEL] prefix (default message exists)|prefix|
|--adm|commits all modules with [ADM] prefix|prefix|
|--wip|commits all modules with [WIP] prefix (default message blank)|prefix|
|--message/-m|commits all modules with the given message|
|--base/-b [git hash]|resets and recommits from [git hash] preserving message for that module|git base|
|--based +n|same as --base but relative commits back from HEAD|git base|
|-p|also push the changes||
|-f|git flag force with lease, force if includes||
|-s|set remote branch from local branch name||
|-n|do not run git hooks||
|-v|verbose||

if no message was provided, the user will be asked one for every module
if no prefix mode was provided, the user will be asked one for every module

## Multitool

refer to [sigil-cli](https://github.com/kenzo-staelens/sigil)