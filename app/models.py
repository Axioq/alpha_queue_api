import json
from pathlib import Path
from collections import OrderedDict

PROGRESS_FILE = Path('progress.json')

def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r')as f:
            return json.load(f)
    return {}

def save_progress(data):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=False)

def get_progress(show_id):
    data = load_progress()
    return data.get(str(show_id))

def update_progress(show_id, season, episode):
    data = load_progress()
    progress_entry = OrderedDict()
    progress_entry['season'] = season
    progress_entry['episode'] = episode
    data[str(show_id)] = progress_entry

    save_progress(data)
    return progress_entry

def delete_progress(show_id):
    data = load_progress()
    removed=  data.pop(str(show_id), None)
    save_progress(data)
    return removed is not None