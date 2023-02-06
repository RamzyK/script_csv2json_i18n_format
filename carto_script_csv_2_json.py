
import csv
import json

# Final dictionnaries that will be tranformed in json
fr_text_dict = []
en_text_dict = []
es_text_dict = []

unsplited_keys = []

static_text_fr_values = {}
static_text_en_values = {}
static_text_es_values = {}

#keys_as_array = []
splited_keys = []
common_values_by_key_roots = {}

# This function will recreate the initial key seperated by '.' to find the value associated in the right language
# @param: splitted_key: Array of strings, which is created by spliting the initial key from the csv file
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



# This function will build a dictionnary to bing common key path to values
## e.g :
##  Key       FR     EN     ES
## a.b.c.d = toto / tutu / titi
## ----- =
## a.b.c.e = toto / tutu / titi
## ----- =
## a.b.c.f = toto / tutu / titi
## ----- =
## a.b.cc  = toto / tutu / titi
## --- ==
## Result -> {('a', 'b', 'c'): ['d', 'e', 'f'], ('a', 'b'): ['cc']}
## With this structur we are able to give the correct level indent in the final lang json structure
def build_dict_of_values_with_same_key_root():
    print(f'Common values dictionnary befor proceesing: {common_values_by_key_roots}')
    for key in splited_keys:
        pos = 0
        key_root = []
        values = []
        while pos < len(key):
            if pos == len(key) - 1:
                values.append(key[pos])
            else:
                key_root.append(key[pos])
            pos += 1
        if tuple(key_root) in common_values_by_key_roots:
            # Add the new values found corresponding to the key's root
            common_values_by_key_roots[tuple(key_root)] = common_values_by_key_roots[tuple(key_root)] + values
        else:
            common_values_by_key_roots[tuple(key_root)] = values
    print(f'Common values dictionnary after proceesing: {common_values_by_key_roots}')


def recc_build_json_representation():
    tail_fr = {
        "text": "toto",
        "accesibilty_description":""
    }
    keys_starting_with_the_same_parent = gather_keys_that_stat_with_the_same_first_parent()
    data = {}

    sub_path_position_start = 1
    loop_count = 0
    for keys_list in keys_starting_with_the_same_parent:
        for key in keys_list:
            key_subpath = key[sub_path_position_start : (len(key))] # Subpath from the root parent of the key
            child_path_object = {}
            try:
                child_path_object = data[key[0]]
            except KeyError as e:
                child_path_object = {}

            if child_path_object:
                if sub_path_position_start < len(key):
                    child_json = build_json_arbo(0, key_subpath, tail_fr)
                    child_json_root = [k for k in child_json][0] # Get the key of the child object already created 
                    recc_position_child_json_correctly(key[0], child_json_root, child_json[child_json_root], data)

                    sub_path_position_start = sub_path_position_start + 1
            else:
                child_json = build_json_arbo(0, key_subpath, tail_fr)
                data[key[0]] = child_json
            loop_count = loop_count + 1
            sub_path_position_start = 1

    print(f'Final JSON: {data}')


def recc_position_child_json_correctly(initial_root, child_root, child, json_file):
    result = {}

    try: 
        result = json_file[initial_root][child_root]
    except KeyError as e:
         json_file[initial_root][child_root] = child

    if result:
        new_json = json_file[initial_root]
        new_initial_root = child_root
        new_child_root = [k for k in child][0]
        new_child = child[new_child_root]
        recc_position_child_json_correctly(new_initial_root, new_child_root, new_child, new_json)
    else:
        json_file[initial_root][child_root] = child

        
    
# Function called to put together keays that start with the same first indentation and
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

def build_json_arbo(position, keys, tail_object):
    #print(f'Reccusrivity working with the list: {keys}')
    if position < len(keys) - 1:
        return {
            keys[position]: build_json_arbo(position + 1, keys, tail_object)
        }
    else:
        tailObj_data = {}
        tailObj_data[keys[position]] = tail_object
        return  tailObj_data
   


def read_and_parse_csv_to_fill_data_structures():
    with open(csv_source_file, "r") as csv_file_handler:
        csv_reader = csv_file_handler.readlines()

        for row in csv_reader:
            columns = row.split(";")
            common_key = columns[0]

            # Split keys to remove point and have array of object level
            unsplited_keys.append(common_key)
            splited_keys.append(common_key.split('.'))
            static_text_fr_values[common_key] = columns[1]
            static_text_en_values[common_key] = columns[2]
            static_text_es_values[common_key] = columns[3]
        
        unsplited_keys.pop(0)
        splited_keys.pop(0)
        
        #print(f'Unsplitted Keys: {unsplited_keys}')
        #print(f'Splitted Keys: {keys_as_array}\n')
        #print(f'FR values: {static_text_fr_values}\n')
        #print(f'EN values: {static_text_en_values}\n')
        #print(f'ES values: {static_text_es_values}\n')

        # Build dictionnary with splitted common key's roots as key and traduction that have the same root as values
        #build_dict_of_values_with_same_key_root()
        recc_build_json_representation()
        if len(static_text_fr_values) == len(static_text_en_values) and  len(static_text_en_values) == len(static_text_es_values):
            print(" Tous les dictionnaires sont avec autant de valeurs")
        else:
            print("Attention toutes les langues n'ont pas le même nombre de mots !")
 
def build_json_objects_for_every_lang():
    for key in common_values_by_key_roots:
        fr_tail_object = {}
        en_tail_object = {}
        es_tail_object = {}
        for value in common_values_by_key_roots[key]:
            formated_tuple = list(key)
            formated_tuple.append(value)
            formated_tuple = tuple(formated_tuple)
        
            tail_fr = {
                "text": static_text_fr_values[compose_key_from_splitted_key_array(formated_tuple)],
                "accesibilty_description":""
            }
            tail_en = {
                "text": static_text_en_values[compose_key_from_splitted_key_array(formated_tuple)],
                "accesibilty_description":""
            }
            tail_es = {
                "text": static_text_es_values[compose_key_from_splitted_key_array(formated_tuple)],
                "accesibilty_description":""
            }
            fr_tail_object[value] = tail_fr
            en_tail_object[value] = tail_en
            es_tail_object[value] = tail_es

        fr_text_dict.append(build_json_arbo(0, key, fr_tail_object))
        en_text_dict.append(build_json_arbo(0, key, en_tail_object))
        es_text_dict.append(build_json_arbo(0, key, es_tail_object))

def csv_to_json():

    read_and_parse_csv_to_fill_data_structures()
    #build_json_objects_for_every_lang()
    
    #write_processed_data_in_fr_json()
    #write_processed_data_in_en_json()
    #write_processed_data_in_es_json()
    
        
def write_processed_data_in_fr_json():
    with open("carto_static_text_fr.json", 'w') as json_file_handler:        
        fr_text_dict.append({"language" :{
            "code": "fr",
            "version": f'{json_file_version}'
        }})
        json_file_handler.write(json.dumps(fr_text_dict, indent = 1, ensure_ascii=False))

def write_processed_data_in_en_json():
    with open("carto_static_text_en.json", 'w') as json_file_handler:        
        en_text_dict.append({"language" :{
            "code": "en",
            "version": f'{json_file_version}'
        }})
        json_file_handler.write(json.dumps(en_text_dict, indent = 1, ensure_ascii=False))

def write_processed_data_in_es_json():
    with open("carto_static_text_es.json", 'w') as json_file_handler:        
        es_text_dict.append({"language" :{
            "code": "es",
            "version": f'{json_file_version}'
        }})
        json_file_handler.write(json.dumps(es_text_dict, indent = 1, ensure_ascii=False))

json_file_version = 1 #input("Version des fichiers json à générer\n") 
# try:
#     int(json_file_version)
# except ValueError as e:
#     json_file_version = 1

csv_source_file = "/Users/kerram/Desktop/Workspace/DEV/Scripts/carto_script/sample_data.csv" #input('Entrez le chemin du fichier CSV depuis lequel vous voulez récupérer les données à insérer dans les fichiers JSON:\n')


csv_to_json()



