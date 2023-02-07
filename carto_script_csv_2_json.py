
# Author : Ramzy KERMAD
# Updated at : 07/02/2023
# Version : 1.0
# Description : Script to generate 3 JSON files from 1 CSV file with 4 rows
#                (Key, TRAD_FR, TRAD_EN, TRAD_ES) 
# Language : Python

import csv
import json
import time
import sys

start_timer = time.perf_counter() # timer when started

COLUMN_SEPARATOR = ";"
KEY_SEPARATOR = "."
LANG_KEY = "language"

FR_TRAD_KEY = "fr"
EN_TRAD_KEY = "en"
ES_TRAD_KEY = "es"

program_finished_successfully = False


## Array containing the keys splitted by their separator
splited_keys = []

dict_key_translation = {}

data_fr = {}
data_en = {}
data_es = {}

# This function will recreate the initial key seperated by '.' to find the value associated in the right language
# @param: splitted_key: [string]--> Array of strings, which is created by spliting the initial key from the csv file
#    e.g: "a.b.c.d" -> ['a', 'b', 'c', 'd']
def compose_key_from_splitted_key_array(splitted_key):
    formatted_key = ""
    pos = 0
    while pos < len(splitted_key):
        if pos != len(splitted_key) - 1:
            formatted_key = f"{formatted_key}{splitted_key[pos]}."
        else:
            formatted_key = f"{formatted_key}{splitted_key[pos]}"
        pos = pos + 1 
    return formatted_key



## Function called to build JSON representation of the CSV file
## @params:
## lang: string --> Language we want to build our JSON file in. the texts in the tail objects will change depending of that
## final_json: {} --> Dictionnary in which we will put our structured data to build the json
def recc_build_json_representation(lang, final_json):
    keys_starting_with_the_same_parent = gather_keys_that_stat_with_the_same_first_parent()

    sub_path_position_start = 1
    loop_count = 0
    for keys_list in keys_starting_with_the_same_parent:
        for key in keys_list:
            text = dict_key_translation[compose_key_from_splitted_key_array(tuple(key))][lang]
            
            tail = {
                "text": text,
                "accesibilty_description":""
            }
            key_subpath = key[sub_path_position_start : (len(key))] # Subpath from the root parent of the key
            child_path_object = {}
            try:
                child_path_object = final_json[key[0]]
            except KeyError as e:
                child_path_object = {}

            if child_path_object:
                if sub_path_position_start < len(key):
                    child_json = build_json_child_arbo(0, key_subpath, tail)
                    child_json_root = [k for k in child_json][0] # Get the key of the child object already created 
                    insert_child_json_in_final_json(key[0], child_json_root, child_json[child_json_root], final_json)

                    sub_path_position_start = sub_path_position_start + 1
            else:
                if len(key) > 1: 
                    child_json = build_json_child_arbo(0, key_subpath, tail)
                    final_json[key[0]] = child_json
                else:
                    final_json[key[0]] = tail
            loop_count = loop_count + 1
            sub_path_position_start = 1


## Function called to insert a child in the JSON tree recursivly
## @params: 
## inital_root: string --> The top first of the first splitted array, it will let us know where we are in the json file arbo
## child_root: string --> Root of the json child we are trying to insert
## child: {} --> JSON object we are trying to insert
## json_file: {} --> Final JSON in which we are' trying to insert a new child
def insert_child_json_in_final_json(initial_root, child_root, child, json_file):
    result = {}

    try: 
        result = json_file[initial_root][child_root]
    except KeyError as e:
         json_file[initial_root][child_root] = child

    if result:
        new_json = json_file[initial_root]
        new_initial_root = child_root
        new_child_root = [k for k in child][0]
        try:
            new_child = child[new_child_root]
            insert_child_json_in_final_json(new_initial_root, new_child_root, new_child, new_json)
        except TypeError as e:
            pass

    else:
        json_file[initial_root][child_root] = child

        
    
# Function called to put together keys that start with the same first indentation and
# returns it back as a list
# e.g: 
## a.b gives the splitted array ['a', 'b']
## aa.b.c gives the splitted array ['aa', 'b', 'c']
## aa.bb.cc gives the splitted array ['aa', 'bb', 'cc']
## d.e.f.g gives the splitted array ['d', 'e', 'f', 'g']
##
## The function return [[['a', 'b']], [['aa', 'b', 'c'], ['aa', 'bb', 'cc']], [['d', 'e', 'f', 'g']]]
## No duplicates are present in the final list
def gather_keys_that_stat_with_the_same_first_parent():
    keys_starting_with_the_same_parent = []
    last_first_parent = ""
    for splited_key in splited_keys:
        first_parent = splited_key[0]
        if last_first_parent != first_parent:
            sorted_splitted_keys = [e for e in splited_keys if first_parent in e]
            keys_starting_with_the_same_parent.append(sorted_splitted_keys)
            last_first_parent = first_parent
    return keys_starting_with_the_same_parent




## Function called to build dictionnary based on list of keys and dependancies in the hierarchy
## @params: 
## position: Represents the position in the keys array to know at which level of depth in the dictionnary we are, it also the terimating check of the reccursive calls
## keys: Array of splitted initial key
## tail_object: Object inserted at the end for the last key
def build_json_child_arbo(position, keys, tail_object):
    if position < len(keys) - 1:
        return {
            keys[position]: build_json_child_arbo(position + 1, keys, tail_object)
        }
    else:
        tailObj_data = {}
        tailObj_data[keys[position]] = tail_object
        return  tailObj_data
   

## Function called to structure the data we will handle. This function extract the info by column et put in in 
## data structure to be processed and to easily interact with.
## It will split the keys by their separator and associate a traduction text to a key
def read_and_parse_csv_to_fill_data_structures():
    global program_finished_successfully
    try:
        with open(csv_source_file, "r") as csv_file_handler:
            csv_reader = csv_file_handler.readlines()

            for row in csv_reader:
                columns = row.split(COLUMN_SEPARATOR)
                common_key = columns[0]

                splited_keys.append(common_key.split(KEY_SEPARATOR))

                dict_key_translation[common_key] = {}
                dict_key_translation[common_key][FR_TRAD_KEY] = columns[1]
                dict_key_translation[common_key][EN_TRAD_KEY] = columns[2]
                dict_key_translation[common_key][ES_TRAD_KEY] = columns[3]
            
            splited_keys.pop(0)
            splited_keys.sort()
    except FileNotFoundError as e:
        print(f"⚠️  Script had problemes during its execution.\n⚠️  Reason : File not found check path \n")
        sys.exit()

 
## Function called to create final json files for the correct lang
def build_json_objects_for_every_lang():
    recc_build_json_representation(FR_TRAD_KEY, data_fr)
    recc_build_json_representation(EN_TRAD_KEY, data_en)
    recc_build_json_representation(ES_TRAD_KEY, data_es)
    

def build_json_file_from_csv_file():

    read_and_parse_csv_to_fill_data_structures()
    build_json_objects_for_every_lang()
    
    write_processed_data_in_fr_json()
    write_processed_data_in_en_json()
    write_processed_data_in_es_json()

    end_timer = time.perf_counter()
    print(f'Script executed in {end_timer - start_timer:0.4f} seconds! 🏎️ 💨')
    
        
def write_processed_data_in_fr_json():
    with open("carto_static_text_fr.json", 'w') as json_file_handler:        
        data_fr[LANG_KEY] = {
            "code": FR_TRAD_KEY,
            "version": f'{json_file_version}'
        }
        json_file_handler.write(json.dumps(data_fr, indent = 2, ensure_ascii=False))
        print(f"🎉 Successfully created and filled JSON file in {FR_TRAD_KEY}! File name: carto_static_text_fr.json")

def write_processed_data_in_en_json():
    with open("carto_static_text_en.json", 'w') as json_file_handler:        
        data_en[LANG_KEY] = {
            "code": EN_TRAD_KEY,
            "version": f'{json_file_version}'
        }
        json_file_handler.write(json.dumps(data_en, indent = 2, ensure_ascii=False))
        print(f"🎉 Successfully created and filled JSON file in {EN_TRAD_KEY}! File name: carto_static_text_en.json")

def write_processed_data_in_es_json():
    with open("carto_static_text_es.json", 'w') as json_file_handler:        
        data_es[LANG_KEY] = {
            "code": ES_TRAD_KEY,
            "version": f'{json_file_version}'
        }
        json_file_handler.write(json.dumps(data_es, indent = 2, ensure_ascii=False))
        print(f"🎉 Successfully created and filled JSON file in {ES_TRAD_KEY}! File name: carto_static_text_es.json")

json_file_version = input("Version des fichiers JSON à générer\n") 
try:
    int(json_file_version)
except ValueError as e:
    json_file_version = 1

csv_source_file = input('Entrez le chemin du fichier CSV depuis lequel vous voulez récupérer les données à insérer dans les fichiers JSON:\n') 

build_json_file_from_csv_file()

