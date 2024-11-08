import re
import argparse
import os
import sys

def extract_soc_data(input_file, verbose=False):
    """
    Extract SOC data from an input file with specific formatting. The code reads each line in the input file, 
    matches the pattern <identifier1|Hso|identifier2,1,0,-1> (cm-1): value1 value2 value3 value4, 
    and extracts 'identifier1-identifier2' as the transition and the second numerical value as the SOC value.
    
    The output file is saved with the input file's base name appended with '_soc_data.dat'.
    """
    # Remove the `.dat` extension and add `_soc_data.dat`
    output_file = f"{input_file.rsplit('.dat', 1)[0]}_soc_data.dat"
    pattern = r"<(\w+)\|Hso\|(\w+),1,0,-1> \(cm-1\):\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)"
    
    # Check if input file exists
    if not os.path.isfile(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        sys.exit(1)
    
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            # Write a header to the output file
            outfile.write("Transition\tValue in cm-1\n")
            if verbose:
                print("Processing file:", input_file)
            
            matches_found = False
            for line in infile:
                match = re.search(pattern, line)
                if match:
                    # Extract identifiers and the second numerical value
                    identifier1 = match.group(1)  # e.g., S0
                    identifier2 = match.group(2)  # e.g., T1
                    value2 = match.group(4)       # the second numerical value
                    
                    transition = f"{identifier1}-{identifier2}"
                    outfile.write(f"{transition}\t\t{value2}\n")
                    matches_found = True
                    
                    if verbose:
                        print(f"Found match: Transition={transition}, Value={value2}")
            
            if not matches_found:
                print("Warning: No matching lines found in the input file.")
                outfile.write("No data extracted.\n")
        
        print(f"Data has been extracted to {output_file}")
    
    except IOError as e:
        print(f"Error: Unable to process files. {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="""
        Extract SOC data from a file and save the results to an output file. 
        
        This code reads an input file with lines in the format:
        <identifier1|Hso|identifier2,1,0,-1> (cm-1): value1 value2 value3 value4
        
        It extracts 'identifier1-identifier2' as the transition and the second numerical value as the SOC value.
        The results are saved in a new file named with '_soc_data.dat' appended to the input file's base name.
        
        Usage:
            python script.py -i input_file.dat [-v]
        """
    )
    parser.add_argument('-i', '--input', required=True, help="Input file name containing SOC data in the specified format")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output for debugging")

    args = parser.parse_args()
    extract_soc_data(args.input, verbose=args.verbose)

if __name__ == "__main__":
    main()
