import json
from git import Repo

repo_path = '' #inserire la path del repository clonato

def get_commits():
    try:
        repo = Repo(repo_path)

        commits = list(repo.iter_commits())

        commit_data = []

        for commit in commits:
            modified_files = commit.stats.files

            files_changed = list(modified_files.keys())

            commit_info = {
                'author': commit.author.name,
                'message': commit.message.strip(),
                'files_changed': files_changed
            }
            commit_data.append(commit_info)

        with open('commit_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(commit_data, json_file, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"Si è verificato un errore: {e}")

get_commits()
