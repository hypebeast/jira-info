#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
from jira import JIRA
from jinja2 import Environment, PackageLoader

import time


ISSUE_TYPE_MAPPING = {
    'features': ['task', 'aufgabe', 'story'],
    'bugs': ['bug']
}

# Jinja2 templates
env = Environment(loader=PackageLoader('jirainfo'),
                    trim_blocks=True,
                    lstrip_blocks=True)


class JiraHelper(object):
    def __init__(self, host, user="", password=""):
        self.host = host
        self.user = user
        self.password = password

        if user != "" and password != "":
            self.jira = JIRA(host, basic_auth=(user, password))
        else:
            self.jira = JIRA(host)

    def getSummary(self, issue):
        """
        Gets the summary for the given ticket.
        """
        issueData = self.jira.issue(issue)
        return issueData.fields.summary

    def getIssues(self, issues):
        """
        Gets the issues from Jira with the given issue numbers.
        """
        result = []
        for issue in issues:
            result.append(self.jira.issue(issue))

        return result


def readIssuesFromInput(input):
    result = []
    for line in input:
        result.append(line.strip(' ').rstrip('\n'))

    return result

def compileEmailTemplate(issues):
    template = env.get_template('email.html')
    return template.render(issues=issues)

def compileChangelogTemplate(features, bugs, others, meta):
    template = env.get_template('changelog.md')
    return template.render(features=features, bugs=bugs, others=others, meta=meta)

@click.group()
@click.option('--host', '-h', envvar="JIRAINFO_HOST", help="Jira server")
@click.option('--user', '-u', envvar="JIRAINFO_USER", help="Username (if required)")
@click.option('--password', '-p', envvar="JIRAINFO_PASS", help="Password (if required)")
@click.pass_context
def cli(ctx, host, user, password):
    """An application that reads information from Jira tickets"""
    if host:
        ctx.obj = JiraHelper(host, user, password)

@cli.command('summary')
@click.argument('input', type=click.File('rb'))
@click.pass_context
def summary(ctx, input):
    """Prints the summary for each ticket"""
    tickets = []
    for line in input:
        tickets.append(line.strip(' ').rstrip('\n'))

    jira = ctx.obj
    results = []
    for ticket in tickets:
        results.append({'title': ticket, 'summary': jira.getSummary(ticket)})

    for line in results:
        click.echo('%s\t%s' % (line['title'], line['summary']))

@cli.command()
@click.argument('input', type=click.File('rb'))
@click.pass_context
def emailreleaselog(ctx, input):
    """Generates a changelog for the release email."""
    jira = ctx.obj

    issueNumbers = readIssuesFromInput(input)
    issues = jira.getIssues(issueNumbers)

    data = []
    for issue in issues:
        link = jira.host + '/browse/' + issue.key
        data.append({'key': issue.key, 'link': link, 'summary': issue.fields.summary})

    output = compileEmailTemplate(data)
    click.echo(output)

@cli.command()
@click.argument('input', type=click.File('rb'))
@click.option('--releasename', '-r', default='Release', help='Release name')
@click.pass_context
def changelog(ctx, input, releasename):
    """
    Generates a changelog for the given issues.
    """
    jira = ctx.obj

    issueKeys = readIssuesFromInput(input)
    issues = jira.getIssues(issueKeys)

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
    output = compileChangelogTemplate(sortedIssues['features'], sortedIssues['bugs'], sortedIssues['others'], meta)
    click.echo(output)

if __name__ == '__main__':
    cli()
