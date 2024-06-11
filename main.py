from nmapscan import nmap_scan
from nmap_xml_to_csv import nmap_xml_to_csv
from combine_csv_to_xlsx import combine_csv_to_xlsx

# Define the target
target = '127.0.0.1'  # Replace with your target

# Call the functions
xml_file_name = nmap_scan(target)
csv_file_name = nmap_xml_to_csv(xml_file_name)

# Combine CSV files into XLSX
xlsx_file_name = combine_csv_to_xlsx([csv_file_name])

print(f"Combined XLSX file created: {xlsx_file_name}")
