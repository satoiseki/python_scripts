import PySimpleGUI as sg
import json
import random
import os

def init_data(filename):
    # TODO: possible exception with different data types / invalid filenames
    if filename != "":
        load_data(filename)

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

def save_data(filename):
    if filename != "":
        clean_data()
        with open(filename, 'w+') as json_file:
            json_file.write(json.dumps(data, indent=4))

def load_data(filename):
    try:    
        with open(filename, 'r') as json_file:
            global data
            data = json.load(json_file)
    except FileNotFoundError:
        save_data(filename)

def clean_data():
    for name in list(data.keys()):
        data[name] = sorted(list(data.fromkeys(data[name])))

### GUI
def init_gui(filename):
    sg.theme('DarkGrey5')

    settings_column = [
        [sg.Text("Settings:", font=("Arial", 18))],
        [sg.Text("Language: ", font=("Arial", 12))],
        [sg.Radio("Any", "RADIO_LANGUAGE", default=True, key="RADIO_LANGUAGE_ANY")],
        [sg.Radio("German", "RADIO_LANGUAGE", default=False, key="RADIO_LANGUAGE_GERMAN")],
        [sg.Radio("Japanese", "RADIO_LANGUAGE", default=False, key="RADIO_LANGUAGE_JAPANESE")],
        [sg.Radio("Korean", "RADIO_LANGUAGE", default=False, key="RADIO_LANGUAGE_KOREAN")],
        [sg.Text("Name by topic: ", font=("Arial", 12))],
        [sg.Radio("Any", "RADIO_TOPIC", default=True, key="RADIO_TOPIC_ANY")],
        [sg.Radio("First Name", "RADIO_TOPIC", default=False, key="RADIO_TOPIC_FIRSTNAME")],
        # [sg.Checkbox("Female", key="FIRST_NAME_FEMALE"), sg.Checkbox("Male", key="FIRST_NAME_MALE")],
        [sg.Radio("Last Name", "RADIO_TOPIC", default=False, key="RADIO_TOPIC_LASTNAME")],
        [sg.Radio("City", "RADIO_TOPIC", default=False, key="RADIO_TOPIC_CITY")],
        [sg.Radio("Country", "RADIO_TOPIC", default=False, key="RADIO_TOPIC_COUNTRY")],
        [sg.Radio("Planet", "RADIO_TOPIC", default=False, key="RADIO_TOPIC_PLANET")],
        [sg.Button('Generate',size=(20,3))],
    ]

    filter_column = [
        [sg.Text("Filter:", font=("Arial", 18))],
        [sg.Text("Number of results:")],
        [
            sg.Radio("5", "RADIO_AMOUNT", default=False, key="RADIO_AMOUNT_5"), 
            sg.Radio("10", "RADIO_AMOUNT", default=True, key="RADIO_AMOUNT_10"), 
            sg.Radio("25", "RADIO_AMOUNT", default=False, key="RADIO_AMOUNT_25"), 
            sg.Radio("50", "RADIO_AMOUNT", default=False, key="RADIO_AMOUNT_50"),
        ],
        [sg.Text("Starts with:")],
        [sg.In(key="input_starts_with", size=(25,2))],
        [sg.Text("Contains:")],
        [sg.In(key="input_contains", size=(25,2))],
        [sg.Text("Ends with:")],
        [sg.In(key="input_ends_with", size=(25,2))],
        [sg.Text("Debug Buttons: ", font=("Arial", 18))],
        [sg.Button('DisplayDB',size=(20,3))],
        [sg.Button('QuitWithoutSaving',size=(20,3))],
    ]

    result_column = [
        [sg.Text("Results:", font=("Arial", 18))],
        [sg.Multiline(autoscroll=True, background_color='grey20', disabled=True, size=(40, 25), font=("Arial", 12), key="textbox")],
    ]

    edit_entry_column = [
        [sg.Text("Edit: ", font=("Arial", 18))],
        [sg.Text("Entry: ")],
        [sg.In(key="input_entry", size=(25,2))],
        [sg.Text("Tag: ")],
        [sg.In(key="input_tag", size=(25,2))],
        [],
        [sg.Button('AddEntry',size=(12,2)), sg.Button('AddTag',size=(12,2))],
        [sg.Button('DeleteEntry',size=(12,2)), sg.Button('DeleteTag',size=(12,2))],
        [sg.Text("Database: ", font=("Arial", 15))],
        [sg.Text("Current database: ")],
        [sg.Text(filename, key="selected_db")],
        [sg.Text("Choose Database: ")],
        [sg.Input(key="input_select_db", visible=False, enable_events=True), sg.FileBrowse(key="input_new_database")],
    ]

    layout = [
        [
            sg.Column(settings_column, vertical_alignment="top"),
            sg.VSeperator(),
            sg.Column(filter_column, vertical_alignment="top"),
            sg.VSeperator(),
            sg.Column(result_column, vertical_alignment="top"),
            sg.VSeperator(),
            sg.Column(edit_entry_column, vertical_alignment="top"),
        ]
    ]

    ### Setting Window
    global window
    window = sg.Window('Name Generator', layout)

    ### Showing the Application and GUI functions

    while True:
        global event
        global values
        global filename_string
        global str_dict

        event, values = window.read()

        if event == sg.WIN_CLOSED:
            save_data(filename_string)
            break
        elif event == "QuitWithoutSaving":
            break
        
        strings_to_use = values["input_entry"].lower().translate(str_dict).split(',')
        tags_to_use = values["input_tag"].lower().translate(str_dict).split(',')

        if event == "Generate":
            text = window["textbox"]
            output = get_output()
            text.update(output)
        elif event == "DisplayDB":
            text = window["textbox"]
            output = json.dumps(data, indent=4)
            text.update(output)
        elif event == "input_select_db":
            filename_string = values["input_new_database"]
            window["selected_db"].update(filename_string)
            load_data(filename_string)
        elif event == "AddEntry":
            add_string_to_data(strings_to_use)
        elif event == "DeleteEntry":
            delete_string_from_data(strings_to_use)
        elif event == "AddTag":
            add_tag_to_string(tags_to_use, strings_to_use)
        elif event == "DeleteTag":
            delete_tag_from_string(tags_to_use, strings_to_use)
        
    window.close()
    ### END GUI

def get_amount():
    output = 0
    for key in values:
        if "RADIO_AMOUNT_" in str(key):
            if values[key] == True:
                return int(key.split('_')[-1])
    return output

def get_output():
    ### TODO: find better alternative to manage the output list to remove element during iteration instead of iterating data repeatedly
    # TODO: add tags/filter for male/female for topic 'firstname'
    output = list(data.keys())
    # Language filter
    if values["RADIO_LANGUAGE_ANY"] == False:
        # Get selected languages
        languages = []
        for key in values:
            if "RADIO_LANGUAGE_" in str(key) and values[key] == True:
                languages.append(key.split('_')[-1].lower())
        # Filter those out with no selected language
        for name in list(data.keys()):
            containsLanguage = False
            for val in data[name]:
                for lang in languages:
                    if val == lang:
                        containsLanguage = True
            if containsLanguage == False:
                output.remove(name)
    # Topic filter
    if values["RADIO_TOPIC_ANY"] == False:
        # Get selected topic
        topic = ""
        for key in values:
            if "RADIO_TOPIC_" in str(key) and values[key] == True:
                topic = key.split('_')[-1].lower()
        # Filter those out without selected topic
        for name in list(data.keys()):
            containsTopic = False
            for val in data[name]:
                if val == topic:
                    containsTopic = True
            if containsTopic == False:
                try:
                    output.remove(name)
                except ValueError:
                    # Already removed from list output
                    pass
    # Contains filter
    for name in list(data.keys()):
        if ((values["input_starts_with"] != "" and
            name.startswith(values["input_starts_with"]) == False) or
            (values["input_ends_with"] != "" and
            name.endswith(values["input_ends_with"]) == False) or
            (values["input_contains"] != "" and
            (values["input_contains"] in name) == False)):
                try:
                    output.remove(name)
                except ValueError:
                    # Already removed from list output
                    pass
    # Reducing to amount by randomly removing names
    for i in range(len(output)-get_amount()):
        output.pop(random.randint(0, len(output)-1))
    return '\n'.join(elem for elem in output)

### Definitions
data = {}
str_dict = str.maketrans("\n ", ",,")
filename_string = "E:\programming\github\stuff\generator_db.txt"

try:
    init_data(filename_string)
    init_gui(filename_string)
except Exception as ex:
    print(ex)
    save_data(filename_string)
    window.close()