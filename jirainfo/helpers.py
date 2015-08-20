# -*- coding: utf-8 -*-

import sys
import click
from jira import JIRAError
from jinja2 import Environment, PackageLoader


# Jinja2 templates
env = Environment(loader=PackageLoader('jirainfo'),
                    trim_blocks=True,
                    lstrip_blocks=True)


def printErrorMsg(msg):
    click.echo(click.style(msg, fg='red'))

def printJiraErrorAndExit(e):
    #errmsg = 'ERROR - Jira error({0}): {1}'.format(e.status_code, e.text)
    errmsg = 'Jira error: {0}'.format(e.status_code)
    printErrorMsg(errmsg)
    sys.exit(1)

def readIssuesFromInput(input):
    result = []
    for line in input:
        result.append(line.strip(' ').rstrip('\n'))

    return result

def getIssuesOrExit(jira, issueKeys):
    try:
        issues = jira.getIssues(issueKeys)
    except JIRAError as e:
        printJiraErrorAndExit(e)

    return issues

def getSummaryOrExit(jira, issueKey):
    try:
        summary = jira.getSummary(issueKey)
    except JIRAError as e:
        printJiraErrorAndExit(e)

    return summary

def compileEmailTemplate(issues):
    template = env.get_template('email.html')
    return template.render(issues=issues)

def compileChangelogTemplate(features, bugs, others, meta):
    template = env.get_template('changelog.md')
    return template.render(features=features, bugs=bugs, others=others, meta=meta)

def exitIfNoHost(ctx):
    errorMsg = """Error: Jira host is not specified! Please, use the --host option or specify the Jira host as an environment variable (JIRAINFO_HOST).
    """
    if not 'host' in ctx.obj or not ctx.obj['host']:
        printErrorMsg(errorMsg)
        #click.echo(ctx.get_help())
        ctx.exit(1)
