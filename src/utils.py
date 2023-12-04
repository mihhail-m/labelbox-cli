import json


def find_active_profile(profiles, key="active", value=True):
    if key in profiles and profiles[key] == value:
        return profiles

    for _, v in profiles.items():
        if isinstance(v, dict):
            result = find_active_profile(v, key, value)
            if result is not None:
                return result


def read_json_file(file_path):
    with open(file_path, "rb") as f:
        return json.load(f)


def write_json_file(file_path, profile):
    with open(file_path, "w+", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=4)
