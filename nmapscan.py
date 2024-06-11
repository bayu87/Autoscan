import nmap

def nmap_scan(scan_target):
    # Initialize the scanner
    nm = nmap.PortScanner()

    # Define the target
    target = scan_target  # Example target, replace with the actual target

    # Run the scan
    nm.scan(target, arguments='-F -sV -O')

    # Save the output to an XML file
    output = nm.get_nmap_last_output()
    decoded_output = output.decode('utf-8')  # Decode the byte string to a regular string

    file_name = f'scan_from_{target}.xml'
    with open(file_name, 'w') as f:
        f.write(decoded_output)  # Write the decoded string to the file

    return file_name
