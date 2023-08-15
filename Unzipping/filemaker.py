import os
from shutil import copy

# Specify the directory containing the PDF files
raw_pdf_path = 'raw_pdf'

# Specify the directory where the folders will be created
folders_path = 'folders'

# Check if the folders directory exists, if not, create it
if not os.path.exists(folders_path):
    os.makedirs(folders_path)

# Iterate through the files in the raw_pdf directory
for filename in os.listdir(raw_pdf_path):
    if filename.endswith('.pdf'):
        # Create folder name based on the PDF file name
        folder_name = os.path.splitext(filename)[0]
        folder_path = os.path.join(folders_path, folder_name)

        # Create the folder
        os.makedirs(folder_path)

        # Optionally, if you want to copy the PDF file into the newly created folder
        source_path = os.path.join(raw_pdf_path, filename)
        destination_path = os.path.join(folder_path, filename)
        copy(source_path, destination_path)

print('Folders created successfully!')
