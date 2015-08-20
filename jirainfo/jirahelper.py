# -*- coding: utf-8 -*-

import click
from jira import JIRA, JIRAError
from jirainfo.helpers import printJiraErrorAndExit, printErrorMsg

class JiraHelper(object):
    def __init__(self, host, user="", password=""):
        self.host = host
        self.user = user
        self.password = password

        try:
            if user != "" and password != "":
                self.jira = JIRA(host, basic_auth=(user, password))
            else:
                self.jira = JIRA(host)
        except JIRAError as e:
            printErrorMsg('Error connecting to %s. Check if username and password are correct.' % (self.host))
            printJiraErrorAndExit(e)

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
