# jira-info

jira-info

## Overview

`jira-info` is an application that helps you to create changelogs from Jira issues and to get some information for Jira issues.

## Features

  * Prints summary information for issues
  * Creates a simple changelog in HTML (e.g. can be used in HTML mails)
  * Creates a detailed changelog in Markdown

## Installation

First, get the latest source code:

    $ git clone https://github.com/hypebeast/jira-info.git

Install it:

    $ cd jira-info
    $ python setup.py install

## Usage

To list all available commands:

    $ jira-info --help

### Env Variables

TODO

### Examples

TODO

## Available Commands

### summary

TODO

### emailreleaselog

TODO

### changelog

TODO


##  Setup a development environment

First, get the latest source code:

    $ git clone https://github.com/hypebeast/jira-info.git

Install dependencies:

    $ cd jira-info
    $ make env

Run it:
  
    $ python bin/jira-info --help

## Contributions

  * Fork repository
  * Create feature- or bugfix-branch
  * Create pull request
  * Use Github Issues

## Contact

  * Sebastian Ruml, <sebastian@sebastianruml.name>
  * Twitter: https://twitter.com/dar4_schneider

## License

```
The MIT License (MIT)

Copyright (c) 2015 Sebastian Ruml

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
