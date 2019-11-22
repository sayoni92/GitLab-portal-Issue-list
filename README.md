# GitLab-portal-Issue-list
 Python script to pull all tickets listed in the GitLab portal


get_issues.py is the main python script which works by first pulling the Issues and then iterating through them one at a time and pulling the Comments for each issue. The output is stored in two formats.  One is a complete dump of the JSON retrieved from GitLab.  The other is a simplified CSV format.
This python script has dependencies on two other scripts, namely business_duration and businesshours.
