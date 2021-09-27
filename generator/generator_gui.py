import PySimpleGUI as sg
import argparse
import random
import generator_dictionary as gd

# Definitions
str_dict = str.maketrans("\n ", ",,")
filename_string = "E:\programming\github\python_scripts\generator\generator_db.txt"

### GUI
def init_gui(filename):
    sg.theme('DarkGrey5')

    settings_column = [
        [sg.Text("Settings:", font=("Arial", 18))],
        [sg.Text("Language: ", font=("Arial", 12))],
        [sg.Combo(list(gd.language_list), default_value=gd.language_list[0], size=(20,1), readonly=True, enable_events=False, key="LANGUAGE_DROPDOWN")],
        [sg.Text("Name by topic: ", font=("Arial", 12))],
        [sg.Combo(list(gd.topic_list), default_value=gd.topic_list[0], size=(20,1), readonly=True, enable_events=False, key="TOPIC_DROPDOWN")],
        [sg.Radio("Female", "FEMALE_VS_MALE", default=True, key="FIRST_NAME_FEMALE"), sg.Radio("Male", "FEMALE_VS_MALE", default=False, key="FIRST_NAME_MALE")],
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
        [sg.Multiline(autoscroll=True, background_color='grey20', disabled=True, size=(30, 25), font=("Arial", 12), key="textbox")],
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
        [sg.Text(filename, size=(25, 3), key="selected_db")],
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
            gd.save_data(filename_string)
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
            output = gd.get_dictionary_dump()
            text.update(output)
        elif event == "input_select_db":
            filename_string = values["input_new_database"]
            window["selected_db"].update(filename_string)
            gd.load_data(filename_string)
        elif event == "AddEntry":
            gd.add_string_to_data(strings_to_use)
        elif event == "DeleteEntry":
            gd.delete_string_from_data(strings_to_use)
        elif event == "AddTag":
            gd.add_tag_to_string(tags_to_use, strings_to_use)
        elif event == "DeleteTag":
            gd.delete_tag_from_string(tags_to_use, strings_to_use)
        
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
    # TODO: split method to the files
    data = gd.data
    output = list(data.keys())
    ## Language filter
    # Get selected languages
    language = values["LANGUAGE_DROPDOWN"].lower().replace(' ', '')
    # Filter those out with no selected language
    if language != "any":
        for name in list(data.keys()):
            containsLanguage = False
            for val in data[name]:
                if val == language:
                    containsLanguage = True
            if containsLanguage == False:
                output.remove(name)
    ## Topic filter
    # Get selected topic
    topic = values["TOPIC_DROPDOWN"].lower().replace(' ', '')
    # Filter those out without selected topic
    if topic != "any":
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

def init():
    try:
        gd.load_data(filename_string)
        init_gui(filename_string)
    except Exception as ex:
        print(ex)

def main():
    #parser = argparse.ArgumentParser()
    #parser.add_argument('-h', '--help', '--HELP')
    #parser.add_argument('-v', dest='verbose', action='store_true')
    #args = parser.parse_args()
    #print(args)
    # ... do something with args.output ...
    # ... do something with args.verbose ..
    init()

if __name__ == '__main__':
    main()