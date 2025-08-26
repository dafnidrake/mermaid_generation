# Import Required Packages
from support_files.letter_generator import LetterCycler
from typing import List, Tuple, Optional
import os
from collections import defaultdict

# Define Module Level Variables
## Define mermaid shapes
O_PG = '('
C_PG = ')'
O_PT = '{{'
C_PT = '}}'
O_FN = '{'
C_FN = '}'
O_ND_S = '[/'
C_ND_S = '/]'
O_ND_W = '[\\'
C_ND_W = '\\]'

## Define mermaid class calls
### Special Node Types
PG = ':::pGrp'
IP_IN = ':::inPort'
IP_OU = ':::outPort'
IP_FP = ':::fp'
FN = ':::fnl'

### Data Inputs
DSR = ':::dsRed'
DSB = ':::dsBlue'
DSPOV = ':::dsPOV'
DSKR = ':::dskafkaRed'
DSKB = ':::dskafkaBlue'
DSKC = ':::dskafkaCirilla'
DSKD = ':::dskafkaDijkstra'
DSKK = ':::dskafkaKahuna'
DSKO = ':::dskafkaOther'
DSC = ':::dsCirilla'
DSR = ':::dsRegis'
DST = ':::dsTriss'
DSO = ':::dsOther'

### Data Outputs
DWF = ':::dwFringilla'
DWC = ':::dwCirilla'
DWK = ':::dwKahuna'
DWD = ':::dwDijkstra'
DWR = ':::dwRegis'
DWT = ':::dwTriss'
DWH = ':::dwHub'
DWS = ':::dwSky'
DWO = ':::dwOther'
DWKR = 'dwKafkaRed'
DWKB = 'dwKafkaBlue'
DWKC = 'dwKafkaCirilla'
DWKD = 'dwKafkaDijkstra'
DWKK = 'dwKafkaKahuna'

## Define mermaid connectors
THICK_LINE = ' === '
START_ARROW = '--'
END_ARROW = '-->'
START_CON = 'o--'
END_CON = '--o'

## Define mermaid file content
INDENT = "  " # set indent to 2 spaces for mermarid file readability
BEGIN_FILE = "```mermaid\ngraph TB;\n" + INDENT + "%% IMPORT_CLASSES %%\n\n"
END_LINE = ';\n'
END_FILE = "\n```"

class MermaidWriter:
    """This class contains the functions necessary to generate the mermaid code 
    syntax needed to produce graphs"""

    def __init__(self):
        self.parent_set = set()
        self.child_set = set()
        self.child_parent = []
        self.child_parent_relation = defaultdict(set)
        
    def write_landing(self, filename, parent, children):
        '''Write out to file the processor group to processor group inteactions on main landing page'''
        
        self.add_pGrp_child_parent(children, parent)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                l_gen = LetterCycler()
                f.write(BEGIN_FILE)
                count = 1
                for child in children:
                    if parent in self.parent_set:
                        pass
                    else:
                        self.parent_set.add(parent)

                    if child in self.child_set:
                        pass
                    else:
                        self.child_set.add(child)
                    
                    if count == 1:
                        letter_1 = self.letter_writer(l_gen)
                        letter_2 = self.letter_writer(l_gen)

                        f.write(INDENT + letter_1 + O_PG + parent + 
                                C_PG + PG + THICK_LINE + letter_2 + 
                                O_PG + child + C_PG + PG + END_LINE)
                        count += 1
                    else:
                        letter_2 = self.letter_writer(l_gen)
                        f.write(INDENT + letter_1 + THICK_LINE + letter_2 + 
                                O_PG + child + C_PG + PG + END_LINE)
                        count += 1

                f.write(END_FILE)
                f.close()
            print(f"Landing page Mermaid code successfully written to '{filename}'.")
        except IOError as e:
            print(f"Error writing to file '{filename}': {e}")

    def letter_writer(self, l_request):
        '''functions gets and returns the last generated letter in sequence of letters
        used to uniquely name processor groups, processors and funnels.'''
        l_request.next_letter()
        latest_letter = l_request.get_last_generated()
        return latest_letter
    
    def find_pGrp_parents(self, data_list: List[Tuple[str, List[str]]], target_child_name: str) -> Optional[str]:
        parent_list = None
        if not parent_list:
            parent_list = []

        for parent_name, child_names_list in data_list:
            if target_child_name in child_names_list:

                if parent_name in parent_list:
                    pass
                else:
                    parent_list.append(parent_name)

        return parent_list

    def get_pGrp_children_groups(self, dict, data_list):
        parent = dict[0]
        children = dict[1]

        for child in children:
            self.child_parent = self.find_pGrp_parents(data_list, child)

        if self.child_parent:
            if parent == 'NiFi Flow':
                landing_filename = "output/landing_page.md"
                self.write_landing(landing_filename, parent, children)
            else:
                self.write_mermaid_code(parent, children, self.child_parent)
        else:
            pass
        
        return parent, children, self.child_parent

    def write_sub_canvas(self, filename, parent, children):
        '''Write out to file the processor group to processor group inteactions on main landing page'''

        self.add_pGrp_child_parent(children, parent)

        main_parent = self.get_pGrp_main_parent(parent)

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                l_wc_gen = LetterCycler()
                f.write(BEGIN_FILE)
                count = 1
                if count == 1:
                    letter_1 = self.letter_writer(l_wc_gen)
                    letter_2 = self.letter_writer(l_wc_gen)

                    f.write(INDENT + letter_1 + O_PG + main_parent + C_PG + 
                            PG + THICK_LINE + letter_2 + O_PG + parent + C_PG +
                            PG + END_LINE)
                    count += 1
                else:
                    for child in children:
                        letter_2 = self.letter_writer(l_wc_gen) 
                        f.write(INDENT + letter_1 + O_PG + 
                                C_PG + THICK_LINE + letter_2 + 
                                O_PG + child + C_PG + PG + END_LINE)
                        count += 1
                f.write(END_FILE)
                f.close()
            print(f"Mermaid code written to processor group canvas '{filename}' successfully.")
        except IOError as e:
            print(f"Error writing to file '{filename}': {e}")

    def write_mermaid_code(self, parent_processor, child_processor_group, parent):
        '''
        Writes a Markdown file with Mermaid code for each child processor group.
        Ensures the directory for the filename exists before writing the file.

        Args:
            parent_processor (str): The parent processor string to be included in the Mermaid code.
            child_processor_group (list): A list of strings, where each string represents
                                          a child processor and will also be used as a directory name.
        '''

        name = parent_processor#['name']

        # Construct the full path to the directory where the .md file will reside.
        output_directory = 'output/' + name 

        # Create the directory if it doesn't exist.
        try:
            os.makedirs(output_directory, exist_ok=True)
        except OSError as e:
            print(f"Error creating directory '{output_directory}': {e}")

        # Construct the full path to the Markdown file.
        file = name + '.md'
        filename = os.path.join(output_directory, file) # Renamed from '.md' to 'diagram.md' for clarity

        self.write_sub_canvas(filename, parent_processor, child_processor_group)

    def add_pGrp_child_parent(self, children, parent):
        if len(children) > 0:
            self.parent_set.add(parent)
        
            for child in children:
                self.child_set.add(child)
                self.child_parent_relation[child].add(parent)
        else:
            for child in children:
                self.child_set.add(child)

        #print("Children Set Includes: ", self.child_set)
        #print("Parent Set Includes: ", self.parent_set)
        return
    
    def print_relation_list(self):

        print("Complete Relationship List:\n", self.child_parent_relation)

    def get_pGrp_main_parent(self, parent):

        main_parent = self.child_parent_relation.get(parent)
        main_parent = next(iter(main_parent))

        return main_parent
        