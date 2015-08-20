#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import click
from jira import JIRAError
from prettytable import PrettyTable
from jirainfo import helpers
from jirainfo.jirahelper import JiraHelper

import time


ISSUE_TYPE_MAPPING = {
    'features': ['task', 'aufgabe', 'story'],
    'bugs': ['bug']
}


@click.group()
@click.option('--host', '-h', envvar="JIRAINFO_HOST", help="Jira host. Env var: JIRAINFO_HOST.")
@click.option('--user', '-u', envvar="JIRAINFO_USER", help="Jira username (optional). Env var: JIRAINFO_USER.")
@click.option('--password', '-p', envvar="JIRAINFO_PASS", help="Jira password (optional). Env var: JIRAINFO_PASS.")
@click.version_option()
@click.pass_context
def cli(ctx, host, user, password):
    """
    jira-info is an application that helps you to create changelogs from Jira issues or to get some additional information for the given issues.

    The issue key are read from stdin and spereated by a line break.

    Note:

    Make sure that a Jira host is specified. Either via the --host option or via the JIRAINFO_HOST environment variable.

    You can also pass the user and password option via environment variables (JIRAINFO_USER, JIRAINFO_PASS).

    Example:

    # This example prints the summary information for the given issues.

    echo 'PROJECT-1234\n,PROJECT-2234\n,PROJECT-3234' > issues.txt

    cat issues.txt | jira-info --host 'http://jira.atlassian.com' --user 'user' -password 'password' summary -
    """
    ctx.obj = {}
    ctx.obj['host'] = host
    ctx.obj['user'] = user
    ctx.obj['password'] = password

@cli.command('summary')
@click.argument('input', type=click.File('rb'))
@click.pass_context
def summary(ctx, input):
    """Prints the summary for each ticket"""
    helpers.exitIfNoHost(ctx)
    jira = JiraHelper(ctx.obj['host'], ctx.obj['user'], ctx.obj['password'])

    tickets = []
    for line in input:
        tickets.append(line.strip(' ').rstrip('\n'))

    results = []
    for ticket in tickets:
        results.append([ticket, helpers.getSummaryOrExit(jira, ticket), jira.host + '/browse/' + ticket])

    x = PrettyTable(["Issue", "Summary", "Link"])
    x.align["Issue"] = "l"
    x.align["Summary"] = "l"
    x.align["Link"] = "l"

    rows = []
    for line in results:
        x.add_row(line)

    click.echo(x)

@cli.command()
@click.argument('input', type=click.File('rb'))
@click.pass_context
def emailreleaselog(ctx, input):
    """Generates a changelog for the release email."""
    helpers.exitIfNoHost(ctx)
    jira = JiraHelper(ctx.obj['host'], ctx.obj['user'], ctx.obj['password'])

    issueNumbers = helpers.readIssuesFromInput(input)
    issues = helpers.getIssuesOrExit(jira, issueNumbers)

    data = []
    for issue in issues:
        link = jira.host + '/browse/' + issue.key
        data.append({'key': issue.key, 'link': link, 'summary': issue.fields.summary})

    output = helpers.compileEmailTemplate(data)
    click.echo(output)

@cli.command()
@click.argument('input', type=click.File('rb'))
@click.option('--releasename', '-r', default='Release', help='The name of the release')
@click.pass_context
def changelog(ctx, input, releasename):
    """
    Generates a changelog for the given issues.
    """
    helpers.exitIfNoHost(ctx)
    jira = JiraHelper(ctx.obj['host'], ctx.obj['user'], ctx.obj['password'])

    issueKeys = helpers.readIssuesFromInput(input)
    issues = helpers.getIssuesOrExit(jira, issueKeys)

    sortedIssues = {}
    sortedIssues['features'] = []
    sortedIssues['bugs'] = []
    sortedIssues['others'] = []

    # Sort issues by type
    for issue in issues:
        issueType = str(issue.fields.issuetype).lower()
        if issueType in ISSUE_TYPE_MAPPING['features']:
            sortedIssues['features'].append(issue)
        elif issueType in ISSUE_TYPE_MAPPING['bugs']:
            sortedIssues['bugs'].append(issue)
        else:
            sortedIssues['others'].append(issue)

    meta = {
            'jira': jira.host,
            'date': time.strftime('%d-%m-%Y', time.gmtime()),
            'releasename': releasename
        }
    output = helpers.compileChangelogTemplate(sortedIssues['features'], sortedIssues['bugs'], sortedIssues['others'], meta)
    click.echo(output)

if __name__ == '__main__':
    # cli({})
    cli()
