import re
import sys
import xml.etree.ElementTree as ET
import csv

# Natural sort function
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    """
    return [atoi(c) for c in re.split(r'(\d+)', text)]

def nmap_xml_to_csv(xml_file_path):
    e = ET.parse(xml_file_path).getroot()

    results = {}
    open_ports = []

    # Iterate through each host
    for host in e.findall('.//host'):
        ptr = ''

        # Get host ip address
        ipaddress = host.find('address').attrib['addr']

        # Get extraports (to show filtered / closed ports)
        try:
            extraports = host.find('.//ports/extraports').attrib['count']
            extraports = extraports + ' '
            extraports = extraports + host.find('ports/extraports').attrib['state']
        except:
            extraports = ''

        # Get PTR for ip address
        for hostname in host.findall('.//hostname'):
            if hostname.attrib['type'] == 'PTR':
                ptr = hostname.attrib['name']

        # Cycle through open ports only - add to 'results' dictionary
        for port_tmp in host.findall('.//port'):
            if port_tmp.find('state').attrib['state'] == 'open':
                if ipaddress not in results.keys():
                    results.update({ipaddress: {'ports': {}}})
                protocol = port_tmp.attrib['protocol']
                port = protocol + port_tmp.attrib['portid']
                open_ports.append(port)
                service = 'open'
                if 'name' in port_tmp.find('service').attrib:
                    service_name = port_tmp.find('service').attrib['name']
                    if 'product' in port_tmp.find('service').attrib:
                        service = port_tmp.find('service').attrib['product']
                        if 'version' in port_tmp.find('service').attrib:
                            service = f"{service} {port_tmp.find('service').attrib['version']}"
                    else:
                        service = service_name
                results[ipaddress]['ports'].update({port: service})

        # If host has open ports - add PTR and extraports to 'results' dict
        if ipaddress in results.keys():
            results[ipaddress].update({'extraports': extraports, 'PTR': ptr})

    # Sort ports using natural ordering
    ports = list(set(open_ports))
    ports = sorted(ports, key=natural_keys)

    # Prepare data for CSV
    csv_data = []
    head = ['ipaddress', 'PTR', 'Other Ports'] + ports
    csv_data.append(head)

    # Cycle through results to print each host as a row
    for ip in results:
        row = [ip, results[ip]['PTR'], results[ip]['extraports']]
        for port in ports:
            row.append(results[ip]['ports'].get(port, ''))
        csv_data.append(row)

    # Define the CSV file name
    csv_file_name = f"{xml_file_path.split('.')[0]}.csv"

    # Write data to CSV file
    with open(csv_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)

    return csv_file_name

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <nmap_xml_file>")
    else:
        csv_file = nmap_xml_to_csv(sys.argv[1])
        print(f"CSV file created: {csv_file}")
