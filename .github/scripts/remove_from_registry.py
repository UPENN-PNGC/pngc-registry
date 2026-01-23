"""
Script to remove a repository from the PNGC registry table in README.md.
Triggered by closing a removal request issue with the 'removal' label.
"""
import os
import re
import requests

README_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'README.md')
GITHUB_REPO = os.environ.get('GITHUB_REPOSITORY')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/issues"


def get_most_recent_removal_issue():
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}', 
        'Accept': 'application/vnd.github+json'
    }
    params = {
        'state': 'closed',
        'labels': 'removal',
        'sort': 'updated',
        'direction': 'desc',
        'per_page': 1
    }
    resp = requests.get(API_URL, headers=headers, params=params)
    resp.raise_for_status()
    issues = resp.json()
    if not issues:
        raise Exception('No closed removal issues found.')
    return issues[0]


def extract_repo_url_from_body(body):
    # Assumes the form field is 'Repository Link:' or similar
    match = re.search(r'Repository Link: ?(https?://github.com/\S+)', body)
    if match:
        return match.group(1).strip()
    # fallback: look for any github.com URL
    match = re.search(r'(https?://github.com/\S+)', body)
    if match:
        return match.group(1).strip()
    raise Exception('Repository link not found in issue body.')


def remove_entry_from_registry(repo_url):
    with open(README_PATH, 'r') as f:
        lines = f.readlines()
    # Find the line containing the repo_url in the registry table
    new_lines = []
    removed = False
    for line in lines:
        if repo_url in line:
            removed = True
            continue  # skip this line
        new_lines.append(line)
    if not removed:
        raise Exception('Repository not found in registry table.')
    with open(README_PATH, 'w') as f:
        f.writelines(new_lines)


def main():
    issue = get_most_recent_removal_issue()
    repo_url = extract_repo_url_from_body(issue['body'])
    remove_entry_from_registry(repo_url)


if __name__ == '__main__':
    main()
