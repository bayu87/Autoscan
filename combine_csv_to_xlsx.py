import pandas as pd
import os

def combine_csv_to_xlsx(csv_files, output_filename='output.xlsx'):
    # Create Excel writer
    writer = pd.ExcelWriter(output_filename)

    # Add custom formatting
    workbook = writer.book
    workbook.formats[0].set_font_size(9)  # Set default font size

    header_format = workbook.add_format()
    header_format.set_font_color('black')
    header_format.set_bg_color('#cccccc')
    header_format.set_bold()

    # Iterate through each CSV file
    for csvfilename in csv_files:
        # Read CSV file into DataFrame
        df = pd.read_csv(csvfilename)
        filename = os.path.splitext(os.path.basename(csvfilename))[0]

        # Write DataFrame to Excel sheet
        df.to_excel(writer, sheet_name=filename, startrow=1, index=False, header=False)

        # Set column width
        for column in df:
            col_idx = df.columns.get_loc(column)
            writer.sheets[filename].set_column(col_idx, col_idx, 15)

        # Write header with header_format
        worksheet = writer.sheets[filename]
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

    # Save and close Excel writer
    writer.close()

    # Return the output filename
    return output_filename
