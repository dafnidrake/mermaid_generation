import subprocess
import os
import re

#Functions
def remove_header(text):
    '''determines the number of colums, creates a regex pattern based on the number of columns. 
    It then removes the header lines and sends it to the extract groups function'''
    lines = text.strip().splitlines()

    delimiter_pattern = r' {2,}[a-zA-Z]'

    num_columns = len(re.split(delimiter_pattern, lines[0],re.I)) + 1

    header = lines[0]

    remove_header = lines[2:]

    pattern_string_start = "^(\\d+)"
    pattern_repeat_part = "({delimiter_regex_str}(.+?))"
    pattern_string_end = "(.*)$"
    pattern_string = pattern_string_start + pattern_repeat_part*(num_columns-1) + pattern_string_end
    
    print(f"Generated Regex Pattern: '{pattern_string}'")

    dict = extract_groups(remove_header, header, pattern_string, num_columns)
    return dict

def extract_groups(text, header, pattern, num_col):
    dict = {}
    col_name = []
    print(text)
    print(pattern)
    print(num_col)
    i = 0
    while i < num_col:
        col_match = pattern.match(header)
        if col_match:
            col_name[i] = match.group(i)
            print(col_name[i])
            i += 1
        else:
           print(f"Warning: Could not parse line: {header.strip()}")

    print(col_name)

    # Go through line by line anhd store in dictionary for later use
    for line in text:
        match = pattern.match(line)
        if match:
            # Extract the matched groups
            index = int(match.group(1))
            name = match.group(2).strip()
            id = match.group(3).strip()
            description = match.group(4).strip()

            # Store as a dictionary: name as key, id as value
            dict[name] = id

        else:
            print(f"Warning: Could not parse line: {line.strip()}")

    return dict

# get baseUrl for command from environment
regURL = os.environ.get("regURL")
propPath = os.environ.get("propPath")

# get location of nifi-toolkit script location
tk = "/home/dafni/Documents/nifi-2.4.0/nifi-toolkit-2.4.0/bin/cli.sh"

# Get buckets from registry by constructing valid ntk command and writing to stdout
registry_buckets = subprocess.run(
    [str(tk), "registry", "list-buckets", "-u", str(regURL)],
    capture_output=True,
    text=True,
    check=False).stdout

print(registry_buckets)

# Get buckets from registry by constructing valid ntk command and writing to stdout
nifi_processor_groups = subprocess.run(
    [str(tk), "nifi", "pg-list", "-p", str(propPath)],
    capture_output=True,
    text=True,
    check=False).stdout

#print(nifi_processor_groups)
# regex used to parse the output
bucket_pattern = re.compile(r'^\s*(\d+)\s+(\S.*?)\s{2,}([0-9a-fA-F-]{36})\s{2,}(.*)')

# remove headers from files
reg_buckets = remove_header(registry_buckets)


# loop through each bucket and get the flow information out
#for bucket_name, bucket_id in reg_buckets.items():
    #print(bucket_name)
    #print(bucket_id)


