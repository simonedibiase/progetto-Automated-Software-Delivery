import json
import re

def contains_keywords(message):
    keywords = ['fix', 'bug'] 
    return any(keyword in message.lower() for keyword in keywords)

with open('filtered_bug_issues.json', 'r', encoding='utf-8') as bug_file:
    bug_data = json.load(bug_file)

with open('commit_data.json', 'r', encoding='utf-8') as commit_file:
    commit_data = json.load(commit_file)

combined_data = []

for commit in commit_data:
    for bug in bug_data:
        conf_sem = 0
        conf_syn = 0

        if re.search(str(bug['number']), commit['message']):
            conf_syn += 1

        if contains_keywords(commit['message']):
            conf_syn += 1

        if re.match(r'^\s*#?[0-9]+\s*$', commit['message']):
            conf_syn += 1

        
        if bug['state'] == 'closed':
            conf_sem += 1

        if bug['title'].lower() in commit['message'].lower():
            conf_sem += 1

        if commit['author'] == bug['assignee']:
            conf_sem += 1

        if conf_sem > 1 or (conf_sem == 1 and conf_syn > 0):
            combined_data.append({
                'bug': {
                    'number': bug['number'],
                    'title': bug['title'],
                    'labels': bug['labels'],
                    'assignee': bug['assignee'],
                    'state': bug['state']
                },
                'commit': {
                    'author': commit['author'],
                    'message': commit['message'],
                    'files_changed': commit['files_changed']
                },
                'conf_sem': conf_sem,
                'conf_syn': conf_syn
            })
            break
            

with open('combined_data.json', 'w', encoding='utf-8') as combined_file:
    json.dump(combined_data, combined_file, indent=2)

print('Dati combinati salvati in combined_data.json')
