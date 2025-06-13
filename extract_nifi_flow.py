import json
import requests
import os

# get Nifi user information from environment
USERNAME = os.environ.get("NIFIUSERNAME")
PASSWORD = os.environ.get("NIFIPASSWORD")
NIFI_URL = os.environ.get("APINIFIURL")

# Define the NiFi server details
#NIFI_URL = 'https://localhost:8443/nifi-api'

# Prompt the user for their username and password
#USERNAME = input("Enter your Nifi username: ")
#PASSWORD = getpass.getpass("Enter your Nifi password: ")  # securely prompt the user for their password without echoing it to the console.

# Define the endpoint for obtaining the token
token_endpoint = f"{NIFI_URL}/access/token"

# Define the headers
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

# Define the payload
payload = {
    'username': USERNAME,
    'password': PASSWORD
}

# Disable warnings for insecure requests (not recommended for production)
requests.packages.urllib3.disable_warnings()


# Separate function to export the gathered details to a JSON file, if desired
def export():
    global root_pg_details
    export_to_json(root_pg_details, 'test_process_group_details.json', output_dir='./nifi-crawl-output')

# Check exported json
def check_exported_file(filename='test_process_group_details.json', output_dir='./nifi-crawl-output'):
    file_path = os.path.join(output_dir, filename)
    if os.path.exists(file_path):
        print(f"File '{file_path}' exists.")
    else:
        print(f"File '{file_path}' does not exist.")

# Function to get the authentication token
def get_token():
    response = requests.post(token_endpoint, headers=headers, data=payload, verify=False)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful
    return response.text.strip()

# Function to get process group details
def get_process_group(process_group_id, token):
    endpoint = f"{NIFI_URL}/flow/process-groups/{process_group_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(endpoint, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()

# Function to get processors for a process group
def get_processors(process_group_id, token):
    endpoint = f"{NIFI_URL}/process-groups/{process_group_id}/processors"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(endpoint, headers=headers, verify=False)
    response.raise_for_status()
    processors = response.json()["processors"]
    return {processor["id"]: {"name": processor["component"]["name"], "id": processor["id"]} for processor in processors}

# Function to get input ports for a process group
def get_input_ports(process_group_id, token):
    endpoint = f"{NIFI_URL}/process-groups/{process_group_id}/input-ports"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(endpoint, headers=headers, verify=False)
    response.raise_for_status()
    input_ports = response.json()["inputPorts"]
    return {port["id"]: {"name": port["component"]["name"], "id": port["id"]} for port in input_ports}

# Function to get output ports for a process group
def get_output_ports(process_group_id, token):
    endpoint = f"{NIFI_URL}/process-groups/{process_group_id}/output-ports"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(endpoint, headers=headers, verify=False)
    response.raise_for_status()
    output_ports = response.json()["outputPorts"]
    return {port["id"]: {"name": port["component"]["name"], "id": port["id"]} for port in output_ports}

# Function to get connections for a process group
def get_connections(process_group_id, token):
    endpoint = f"{NIFI_URL}/process-groups/{process_group_id}/connections"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(endpoint, headers=headers, verify=False)
    response.raise_for_status()
    connections = response.json()["connections"]
    
    connections_list = [
        {
            "source": connection["component"]["source"]["name"],
            "source_type": connection["component"]["source"]["type"],
            "source_id": connection["component"]["source"]["id"],
            "destination": connection["component"]["destination"]["name"],
            "destination_type": connection["component"]["destination"]["type"],
            "destination_id": connection["component"]["destination"]["id"],
            "relationship": connection["component"].get("selectedRelationships", [])
        }
        for connection in connections
    ]

    # Ensure connections are sorted by source name, then by destination name
    connections_list.sort(key=lambda x: (x["source"], x["destination"]))
    
    return connections_list

# Function to get child process groups for a process group
def get_child_process_groups(process_group_id, token):
    endpoint = f"{NIFI_URL}/process-groups/{process_group_id}/process-groups"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(endpoint, headers=headers, verify=False)
    response.raise_for_status()
    child_pgs = response.json()["processGroups"]
    return {child_pg["id"]: {"name": child_pg["component"]["name"], "id": child_pg["id"]} for child_pg in child_pgs}, child_pgs

# Recursive function to gather all details for process groups and their components
def gather_process_group_details(process_group_id, token):
    details = {}

    # Get process group details
    pg_details = get_process_group(process_group_id, token)
    details['name'] = pg_details['processGroupFlow']['breadcrumb']['breadcrumb']['name']
    details['id'] = process_group_id

    # Get processors
    processors = get_processors(process_group_id, token)
    details['processors'] = list(processors.values())

    # Get input ports
    input_ports = get_input_ports(process_group_id, token)
    details['input_ports'] = list(input_ports.values())

    # Get output ports
    output_ports = get_output_ports(process_group_id, token)
    details['output_ports'] = list(output_ports.values())

    # Get connections
    details['connections'] = get_connections(process_group_id, token)

    # Get child process groups and their details recursively
    details['child_process_groups'] = []
    child_pg_names, child_pgs = get_child_process_groups(process_group_id, token)
    for child_pg in child_pgs:
        child_pg_details = gather_process_group_details(child_pg['id'], token)
        details['child_process_groups'].append(child_pg_details)

    return details

# Function to export details to a JSON file
def export_to_json(data, filename='test_process_group_details.json', output_dir='./nifi-crawl-output'):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Construct the full file path
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Process group details have been exported to '{file_path}'.")

# Main function to initiate data gathering and printing
def main():
    try:
        token = get_token()
        print(f'Successfully retrieved token.')

        # Start with the root process group
        root_pg_id = 'root'
        global root_pg_details
        root_pg_details = gather_process_group_details(root_pg_id, token)

        # Print the gathered details in pretty JSON format
        print("Process Group Details:")
        #print(json.dumps(root_pg_details, indent=4))

        export()
    except Exception as e:
        print(f'An error occurred: {e}')

    # Check if the file exists
    #check_exported_file()

if __name__ == '__main__':
    main()

