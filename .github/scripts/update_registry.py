"""
Script to update the PNGC partner project registry table in README.md.
Fetches the most recent closed issue with the 'registration' label using the GitHub API,
parses its body, and adds the entry to the registry table.
"""
import os
import re
import requests

README_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'README.md')

GITHUB_REPO = os.environ.get('GITHUB_REPOSITORY')  # e.g., 'UPENN-PNGC/pngc-partner-projects'
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/issues"

def get_most_recent_registration_issue():
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    params = {
        'state': 'closed',
        'labels': 'registration',
        'sort': 'updated',
        'direction': 'desc',
        'per_page': 1
    }
    resp = requests.get(API_URL, headers=headers, params=params)
    resp.raise_for_status()
    issues = resp.json()
    if not issues:
        raise Exception('No closed registration issues found.')
    return issues[0]

def parse_issue_body(body):
    # Map form fields to table columns, including Funding and Additional Info
    def extract(field):
        pattern = rf"{field}: ?(.+?)(?:\n|$)"
        match = re.search(pattern, body, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return ''

    lab = extract('Lab / Group Name')
    repo_url = extract('Repository Link')
    repo_name = repo_url.rstrip('/').split('/')[-1] if repo_url else ''
    description = extract('Description')
    contact = extract('Primary Contact')
    category = extract('Category')
    license_ = extract('License')
    published = extract('Has this work been published?')
    publication = extract('DOI or PubMed Link') if published.lower() == 'yes' else ''
    status = extract('Repository Status')
    funding = extract('Funding Acknowledgment')
    # Additional Info field removed from table

    return [
        lab,
        f'[{repo_name}]({repo_url})' if repo_url and repo_name else '',
        description,
        contact,
        category,
        license_,
        publication,
        status,
        funding
    ]

def update_registry_table(new_entry):
    with open(README_PATH, 'r') as f:
        content = f.read()
    # Find the registry table and insert the new entry after the header
    pattern = r"(\| Lab/Group .+?\| Status \|\n\|[-|]+\|\n)"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        raise Exception('Registry table header not found in README.md')
    table_header = match.group(1)
    new_row = '| ' + ' | '.join(new_entry) + ' |\n'
    # Insert new row after header
    updated_content = content.replace(table_header, table_header + new_row)
    with open(README_PATH, 'w') as f:
        f.write(updated_content)

def main():
    issue = get_most_recent_registration_issue()
    new_entry = parse_issue_body(issue['body'])
    update_registry_table(new_entry)

if __name__ == '__main__':
    main()
