import os

#this script goes through all the files ending with fbx.meta checks if Gen lightmap UVs is turned on. if yes it's subsequent .fbx filepath is added to an output file

def find_fbx_meta_files_with_secondary_uv(folder_path, output_file):
    # List to store the file paths
    fbx_files_with_secondary_uv = []

    # Traverse the folder and its subfolders
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.fbx.meta'):
                file_path = os.path.join(root, file)
                
                # Read the file to check for generateSecondaryUV: 1 this is value for Generate lightmap UVs in the meta file
                with open(file_path, 'r') as f:
                    content = f.read()
                    if 'generateSecondaryUV: 1' in content:
                        # Remove the .meta suffix and add to the list
                        fbx_file_path = file_path[:-5]  # Removing '.meta'
                        fbx_files_with_secondary_uv.append(fbx_file_path)

                        # Update generateSecondaryUV: 1 to generateSecondaryUV: 0
                        updated_content = content.replace('generateSecondaryUV: 1', 'generateSecondaryUV: 0')
                        with open(file_path, 'w') as f:
                            f.write(updated_content)

    # Write the collected file paths to the output file
    with open(output_file, 'w') as output:
        for path in fbx_files_with_secondary_uv:
            output.write(path + '\n')

if __name__ == "__main__":
    # Get the current working directory
    current_folder = os.getcwd()
    
    # Define the output file name
    output_file = os.path.join(current_folder, 'output_file.txt')
    
    # Call the function with the current folder and output file
    find_fbx_meta_files_with_secondary_uv(current_folder, output_file)
    
    print(f'Results written to {output_file}')

