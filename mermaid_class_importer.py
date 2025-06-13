import os
import sys # Import sys to get the script's path

def generate_mermaid_chart(template_filepath, common_classes_content, output_filepath, indent_spaces=4, placeholder='%% IMPORT_CLASSES %%'):
    """
    Generates a formatted Mermaid chart by importing common class definitions found in 
    common_classes.md and applying a consistent indentation to output mermaid charts. 
    Make changes to mermaid charts in base_charts directory then execute python script 
    mermaid_class_importer.py to produce updated formatted charts. If you make
    changes to charts in the formatted_charts directory, they will be overwritten
    on the next execution of the python script.

    Args:
        template_filepath (str): Full path to the unformatted Mermaid template files in base_charts/
        common_classes_content (str): The content of the common classDef statements
        output_filepath (str): Full path where the final formatted Mermaid chart will be saved formatted_charts/
        indent_spaces (int): The number of spaces to indent the imported lines currently set to 4
        placeholder (str): The placeholder string to replace in the template currently set to %% IMPORT_CLASSES %%
    """

    # Attempt to locate template mermaid chart files
    try:
        with open(template_filepath, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found: {template_filepath}")
        return
    except Exception as e:
        print(f"Error reading template file {template_filepath}: {e}")
        return

    # Create the indentation string
    indentation = ' ' * indent_spaces

    # Process each line from the common_classes.md file content
    indented_class_lines = []
    for line in common_classes_content.split('\n'):
        stripped_line = line.strip()

        if stripped_line:
            indented_class_lines.append(indentation + stripped_line)

    indented_class_block = '\n'.join(indented_class_lines)

    # Replace the placeholder with the consistently indented common classes
    # Ensure a newline before and after the block for clean embedding
    final_content = template_content.replace(placeholder, '\n' + indented_class_block + '\n')

    # Ensure the output directory for this specific file exists
    output_dir = os.path.dirname(output_filepath)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}") # Inform user about new directories

    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f"Generated: {output_filepath}")
    except Exception as e:
        print(f"Error writing output file {output_filepath}: {e}")


if __name__ == "__main__":
    # Determine the script's absolute directory
    # This gets the directory where *this script* (mermaid_class_importer.py) is located.
    # It works regardless of the Current Working Directory.
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Configuration: All paths are relative to the script's directory
    COMMON_CLASSES_FILE = os.path.join(script_dir, 'common_classes.md')
    INPUT_DIR = os.path.join(script_dir, 'base_charts')
    OUTPUT_DIR = os.path.join(script_dir, 'formatted_charts')

    INDENT_SPACES = 2
    TEMPLATE_PLACEHOLDER = '%% IMPORT_CLASSES %%'
    FILE_EXTENSIONS = ('.md')

    # Load Common Classes Once
    try:
        with open(COMMON_CLASSES_FILE, 'r', encoding='utf-8') as f:
            common_classes_content = f.read()
        print(f"Successfully loaded common classes from: {COMMON_CLASSES_FILE}")
    except FileNotFoundError:
        print(f"Error: Common classes file '{COMMON_CLASSES_FILE}' not found. Please ensure it exists.")
        exit(1)
    except Exception as e:
        print(f"Error reading common classes file '{COMMON_CLASSES_FILE}': {e}")
        exit(1)

    # Create Top-Level Output Directory if it doesn't exist
    # os.makedirs with exist_ok=True avoids an error if the directory already exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        print(f"Created top-level output directory: {OUTPUT_DIR}")

    # Process Files in Directory Tree
    processed_count = 0
    print(f"\nStarting to process files from '{INPUT_DIR}' to '{OUTPUT_DIR}'...")

    # os.walk yields (dirpath, dirnames, filenames) for each directory it visits
    for root, dirs, files in os.walk(INPUT_DIR):
        # Calculate the relative path from INPUT_DIR to the current 'root'
        # This part still assumes the relative structure *within* the input_charts folder
        relative_path = os.path.relpath(root, INPUT_DIR)

        # Construct the corresponding output directory path relative to the SCRIPT'S output dir
        current_output_dir = os.path.join(OUTPUT_DIR, relative_path)

        # Go through each file found and produce formatted chart
        for filename in files:
            if filename.lower().endswith(FILE_EXTENSIONS):
                template_filepath = os.path.join(root, filename)
                output_filepath = os.path.join(current_output_dir, filename)

                generate_mermaid_chart(
                    template_filepath,
                    common_classes_content,
                    output_filepath,
                    indent_spaces=INDENT_SPACES,
                    placeholder=TEMPLATE_PLACEHOLDER
                )
                processed_count += 1

    # Give user information about what was processed
    print(f"\nProcessing complete. {processed_count} Mermaid charts generated in '{OUTPUT_DIR}'.")
    if processed_count == 0:
        print("No files matching the specified extensions were found.")