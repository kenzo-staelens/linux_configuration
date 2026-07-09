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

generic tool to quickly generate nested commands/scripts based on yaml

### Syntax

This module uses yaml files to generate configuration and is split into 3 different syntax modes

#### Manifest

The root of a command is defined by a file named `.manifest.yml`
a manifest contains a list of sub-files to include, the tool will internally join them all into one large file before processing all definitions (this makes it possible to use the same arguemt across multiple files, see section arguments)

#### Subcommand Command

A command is defined as

```yaml
internal_id:
    name: (sub)command name
    python import format
    help: help message for this subcommand
    script_dir: directory where script files are found in dotted (only used by root)
    default: (optional) whether this is the default subcommand in it's parent, last defined wins 
    script: script file (basename) to run when executing this subcommand
    args:
        - list of argument definitions, anchors
        - or left blank (see section arguments)
```

note: script_dir is relative to the python file executing this configuration (eg. in this repo: relative to multitool.py in at the root of this repo)

at least one id 'root' must be defined, this is the first node processed by this tool.

##### examples

```yaml
# root section definition
root:
  name: multitool  # command line name
  script_dir: multitool_files  # where to find scripts
  args:  # no args, may be empty or omitted
```

```yaml
# subcommand
rebase:  # id is rebase
  name: rebase  # command line name
  parent: root  # refrences id of root command
  help: command utility to automate changelog rebases  # text in root help menu
  default: false
  script: autorb  # script to run, stored in $script_dir/autorb.py
  args:
    - *rebase_target  # list of argument (yaml reference, see argument section)
```

#### arguments

because just having commands without arguments is kind of useless adding arguments to a configuration is also supported, it is defined mostly as to how argparse consumes argument definitions

```yaml
# title here only exists to create logical grouping in yaml
instance_reset_dbfile: &rebase_target  # followed by optional anchor
  !arg  # required custom tag to generate argument from definition
  name:  # name or names of the target as passed to argparse
    - -t
    - --target
  help: target project to rebase  # help message
  required: true  # whether the arg is required
  # default: "default value for the argument"

snapshot_arg_s3: &snapshot_arg_s3
  !arg
  name:
    - --s3
  action: store_true  # arguments may be boolean too with store_true/store_false
  help: Upload to or Download from s3
  # more argparse compatible arguments allowed
  # argcomplete -> completer not yet supported
```

args must be either directly defined in the subcommand argument list or via reference (for ease of development i *highly* recommend by reference)

#### scripts

scripts only have 1 requirement, somewhere (top level) in the python file they need to expose

```python
def run(args: Namespace, ctx: dict[str, Any]):
    ...
```

ctx is a dictionary that gets passed on to every script encountered in order, you can write, modify and delete values in context to pass extra arguments or whatever else you like to subsequent scripts

args contains the parsed arguments for the currently executing command (as defined by argparse)

all encountered scripts throughout the entire command path (i.e. all scripts on it's subparsers) are executed in the order the subcommand is encountered.
