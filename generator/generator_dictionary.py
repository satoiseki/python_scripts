import json

data = {}
language_list = ["Any", "German", "Japanese", "Korean"]
topic_list = ["Any", "First Name", "Last Name", "City", "Country", "Planet"]

## dictionary methods

def add_string_to_data(strings_to_add):
    for name in strings_to_add:
        if name != "" and data.get(name, None) == None:
            data[name] = []

def add_tag_to_string(tags_to_add, strings_to_use):
    for name in strings_to_use:
        if name != "":
            try:
                for tag in tags_to_add:
                    if tag != "":
                        data[name].append(tag)
            except KeyError as ke:
                print(ke)
                add_string_to_data([name])
                for tag in tags_to_add:
                    if tag != "":
                        data[name].append(tag)

def delete_string_from_data(strings_to_delete):
    for name in strings_to_delete:
        data.pop(name, None)

def delete_tag_from_string(tags_to_delete, strings_to_use):
    for name in strings_to_use:
        for tag in tags_to_delete:
            try:
                data[name].remove(tag)
            except (KeyError, ValueError):
                pass

## file operations

def save_data(filename):
    if filename != "":
        try:
            clean_data()
            with open(filename, 'w+') as json_file:
                json_file.write(json.dumps(data, indent=4))
        except FileNotFoundError:
            pass

def load_data(filename):
    if filename != "":
        try:
            with open(filename, 'r') as json_file:
                global data
                data = json.load(json_file)
        except FileNotFoundError:
            pass

def clean_data():
    for name in list(data.keys()):
        data[name] = sorted(list(data.fromkeys(data[name])))

## getter

def get_dictionary_dump():
    return json.dumps(data, indent=4)