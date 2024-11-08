import json
from collections import Counter

with open('combined_data.json', 'r', encoding='utf-8') as updated_file:
    updated_data = json.load(updated_file)

file_counter = Counter()

for entry in updated_data:
    commit = entry['commit']
    files_changed = commit.get('files_changed', [])
    file_counter.update(files_changed)

most_common_files = file_counter.most_common(10)

result = [{"file": file, "count": count} for file, count in most_common_files]

with open('top_10_files_changed.json', 'w', encoding='utf-8') as output_file:
    json.dump(result, output_file, indent=2)

print('I 10 file più presenti in files_changed sono stati salvati in top_10_files_changed.json')
