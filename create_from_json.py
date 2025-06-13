# Import Required Packages
import json
from support_files.writing_logic import MermaidWriter
from typing import List, Any

# Functions
def read_json_dict(file_path):
    '''Read Json data in as a dictionary'''
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{file_path}'. Check for malformed JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    #pretty_json_output = json.dumps(data, indent=4)
    #print(pretty_json_output)
    return data

def get_all_parent_child(data):
    # Get parent processor name
    parent_processor_name = data.get("name") 

    # Get all names from "child_process_groups"
    child_group_names = []
    child_process_groups = data.get("child_process_groups", [])

    for group in child_process_groups:
        group_name = group.get("name")
        if group_name: # Ensure the 'name' key exists
            child_group_names.append(group_name)

    return parent_processor_name, child_group_names

def search_all_dictionaries(dict_list):
    '''searches for a key and iterates through list of nested dictionaries'''
    parents = []
    my_dict = dict_list[0]
        
    child_group = my_dict.get('child_process_groups')

    if child_group and isinstance(child_group, list) and len(child_group) > 0:
        parents.append(get_all_parent_child(my_dict))
            
    for item in child_group:
        if child_group and isinstance(child_group, list) and len(child_group) > 0:
            parents.append(get_all_parent_child(item))

    return parents

def find_top_dict_containing_key(data, target_key):
    """
    Finds the top most level dictionary that contain the target_key in a nested
    dictionary or list structure.

    Args:
        data (dict or list): The dictionary or list to search within.
        target_key (str): The key whose containing dictionaries are to be extracted.

    Returns:
        list: A list containing all dictionaries where the target_key is found.
              Returns an empty list if the key is not found or data is not
              a dict/list.
    """
    found_dicts = []

    # If the current 'data' is a dictionary
    if isinstance(data, dict):
        # Check if the target_key is directly in the current dictionary
        if target_key in data:
            found_dicts.append(data) # Add the dictionary itself to the results

    return found_dicts
            
def remove_empty_lists_recursive(nested_list: List[Any], prune_immediate_empty_lists: bool = True) -> List[Any]:
    """
    Recursively processes a nested list structure to remove empty lists.

    Behaves as follows:
    - If `prune_immediate_empty_lists` is True (default for initial call):
      Removes empty lists (`[]`) that are direct children of the current `nested_list`.
    - If `prune_immediate_empty_lists` is False (for recursive calls on sub-lists):
      Keeps empty lists (`[]`) that are direct children of the current `nested_list`.

    Args:
        nested_list (List[Any]): The list to process, potentially containing
                                  other lists and non-list elements.
        prune_immediate_empty_lists (bool): If True, removes empty lists
                                             that are direct children at this level.
                                             Defaults to True for the initial call.

    Returns:
        List[Any]: A new list with empty sub-lists handled according to the logic.
                   Returns an empty list if the input was empty or contained
                   only empty lists at the top-most level.
    """
    if not isinstance(nested_list, list):
        # If the input is not a list, return it as is.
        return nested_list

    filtered_list = []
    for item in nested_list:
        if isinstance(item, list):
            # If the current item is an empty list and we are in pruning mode for this level, skip it.
            if prune_immediate_empty_lists and item == []:
                continue
            else:
                # Crucially, we pass prune_immediate_empty_lists=False to the recursive call
                # to ensure that empty lists *inside* this sub-list are NOT removed
                processed_sublist = remove_empty_lists_recursive(item, prune_immediate_empty_lists=False)
                # Always append the result of the recursion in this branch,
                # as the decision to prune the original 'item' was already made above.
                filtered_list.append(processed_sublist)
        else:
            # If the item is not a list, directly add it to the result
            filtered_list.append(item)

    # If this list became empty after filtering AND it was meant to be pruned
    # then return an empty list. Otherwise, return the filtered_list.
    if prune_immediate_empty_lists and not filtered_list:
        return []
    
    final_processor_groups = []
    if len(filtered_list) == 1 and isinstance(filtered_list[0], list):
        final_processor_groups = filtered_list[0]
    else:
        final_processor_groups = filtered_list 
    return final_processor_groups


if __name__ == '__main__':
    writer = MermaidWriter()

    # Json file location
    file_path = 'nifi-crawl-output/test_process_group_details.json'

    # Read in json data file
    data = read_json_dict(file_path)

    # Search through data and find all nested dictionaries
    all_dicts = find_top_dict_containing_key(data, 'name')

    # Iterate through all dictionaries and find relevant info
    parent_processor_groups = list(search_all_dictionaries(all_dicts))

    # Clean out any completely empty list values
    clean_list = remove_empty_lists_recursive(parent_processor_groups)

    # Build all relationships and initiate code generation
    for item in clean_list:
        writer.get_children_groups(item, clean_list)

    # Print out complete relationship dictionary
    writer.print_relation_list()