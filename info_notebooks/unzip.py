import gzip
import os

# Set the input and output directory paths
input_dir = "./data"
output_dir = "./unzipped_data"

# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    # Check if the file is a .gzip file
    if filename.endswith(".gzip"):
        # Open the compressed file in binary mode
        with gzip.open(os.path.join(input_dir, filename), 'rb') as f:
            # Read the contents of the compressed file
            file_contents = f.read()
        # Create a new file in the output directory with the same name as the original file
        with open(os.path.join(output_dir, filename[:-5]), 'wb') as f:
            # Write the uncompressed contents to the new file
            f.write(file_contents)
