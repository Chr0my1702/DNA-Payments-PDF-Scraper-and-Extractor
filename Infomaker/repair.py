import os
import subprocess

input_directory = 'master'
output_directory = 'repaied'

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Iterate through all PDF files in the directory
for filename in os.listdir(input_directory):
    if filename.endswith('.pdf'):
        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, filename)
        
        # Call Ghostscript to reprocess the PDF
        command = f'gswin64c -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -o "{output_path}" "{input_path}"'
        result = subprocess.run(command, shell=True)

        # Check if Ghostscript ran successfully
        if result.returncode != 0:
            print(f'Failed to repair {input_path}')
        else:
            print(f'Successfully repaired {input_path}')
