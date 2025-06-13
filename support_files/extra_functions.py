def find_first_key_value(data, target_key):
    '''Function finds the first key in dictionary'''
    if isinstance(data, dict):
        if target_key in data:
            return data[target_key]
        for key, value in data.items():
            result = find_first_key_value(value, target_key)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_first_key_value(item, target_key)
            if result is not None:
                return result
    return None

def find_all_values_for_key(data, target_key):

    """
    Recursively finds all values associated with a given key in a nested
    dictionary or list and stores them in a list.
    """
    found_values = []

    if isinstance(data, dict):
        # If the current data is a dictionary
        for key, value in data.items():
            if key == target_key:
                found_values.append(value)
            # Recursively call for nested dictionaries or lists
            found_values.extend(find_all_values_for_key(value, target_key))
    elif isinstance(data, list):
        # If the current data is a list, iterate through its elements
        for item in data:
            found_values.extend(find_all_values_for_key(item, target_key))

    return found_values