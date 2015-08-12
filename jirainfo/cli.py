#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
from jira import JIRA
from jinja2 import Environment, FileSystemLoader, Template

from templates import EMAIL_TEMPLATE


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

def compileTemplate(issues, template):
    if not template:
        raise ValueError("a template must be given")

    template = Template(template)
    return template.render(issues=issues)


@click.group()
@click.option('--host', '-h', envvar="JIRAINFO_HOST", help="")
@click.option('--user', '-u', envvar="JIRAINFO_USER", help="")
@click.option('--password', '-p', envvar="JIRAINFO_PASS", help="")
@click.pass_context
def cli(ctx, host, user, password):
    """An application that reads information from Jira tickets"""
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

    output = compileTemplate(data, EMAIL_TEMPLATE)
    click.echo(output)


if __name__ == '__main__':
    cli()
