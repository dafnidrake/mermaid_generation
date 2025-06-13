# Import packages
import re
import os
import sys

# Define Functions
def find_files(script_dir, input_dir, file_ext):
    processed_count = 0
    print(f"Starting from '{input_dir}'...\n")

    file_list = []

    for root, dir, files in os.walk(input_dir):
        relative_path = os.path.relpath(root, input_dir)

        for filename in files:
            if filename.endswidth(file_ext):
                file_path = os.path.join(relative_path, filename)
                file_list.append(file_path)
                processed_count += 1
    
    print(f"{processed_count}{file_ext} were found and processed.")

    if processed_count == 0:
        print("No files were found to process")

    return file_list

def find_replace_text(text, pattern, replacement, count=0, flags=0):
    try:
        compiled_pattern = re.compile(pattern, flags)
        modified_text = compiled_pattern.sub(replacement, text, count)

        return modified_text
    
    except re.error as e:
        print(f"Text and pattern not found {e}.")
    
        return text
    
def open_text(text):
    try:
        with open(text, 'r', encoding='utf-8') as f:
            content = f.read()
            return content
    
    except FileNotFoundError:
        print(f"Error: File '{text}' not found.")
        exit(1)

    except Exception as e:
        print(f"Error reading '{text}':'{e}'")
        exit(1)

def close_text(text, result):
    with open(text, 'w', encoding='utf-8') as f:
        f.write(result)
        f.close()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, 'base_charts')
    file_ext = '.md'

    filepaths = find_files(script_dir, input_dir, file_ext)

    replacement_map = {
        r':::processorGroup': r':::pGrp',
        r':::dataSource': r':::ds',
        r':::dataWrite': r':::dw'
    }

    for filepath in filepaths:
        if filepath.startswith('./'):
            filepath = os.path.join(input_dir + filepath[1:])
        
        else:
            filepath = os.path.join(input_dir + '/' + filepath)

    original_text = open_text(filepath)
    processed_text = original_text

    for pattern, replacement in replacement_map.items():
        processed_text = find_replace_text(processed_text, pattern, replacement)

    if processed_text != None:
        close_text(filepath, processed_text)

        # need a test portion here for new regexes

    else:
        print('No text was replaced.')

    if __name__ == "__main__":
        main()