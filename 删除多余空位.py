import csv

# Define the input and output file paths
input_file_path = 'C:\\Users\\aaqqi\\Desktop\\6140_Final\\MachineLearning_FictionPopularityPrediction\\JinjiangBooksNew.csv'
output_file_path = 'C:\\Users\\aaqqi\\Desktop\\6140_Final\\MachineLearning_FictionPopularityPrediction\\CleanedJinjiangBooksNew.csv'

# Read the data, omit the 11th column, and write to a new CSV file
with open(input_file_path, 'r', newline='', encoding='utf-8') as infile, \
     open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # Read the header and write it directly to the output file
    headers = next(reader)
    writer.writerow(headers)  # Write headers without modification

    # Process each data row, removing the 11th column
    for row in reader:
        # Remove the empty 11th column (index 10 because Python uses 0-based indexing)
        new_row = row[:10] + row[11:]
        writer.writerow(new_row)

print("The CSV file has been cleaned and saved without the empty column.")
