import os

#this script goes through all the files ending with fbx.meta checks if  material import mode is set to import then sets it to none

def find_fbx_meta_files_with_secondary_uv(folder_path, output_file):
    fbx_files_with_secondary_uv = []

    # Traverse the folder and its subfolders
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.fbx.meta'):
                file_path = os.path.join(root, file)
                
                # Read the file to check for generateSecondaryUV: 1 this is value for Generate lightmap UVs in the meta file
                with open(file_path, 'r') as f:
                    content = f.read()
                    if 'materialImportMode: 2' in content:
                        # Remove the .meta suffix and add to the list
                        fbx_file_path = file_path[:-5]  # Removing '.meta'
                        fbx_files_with_secondary_uv.append(fbx_file_path)

                        #set material import mode to none
                        updated_content = content.replace('materialImportMode: 2', 'materialImportMode: 0')
                        with open(file_path, 'w') as f:
                            f.write(updated_content)
                            print('-- File Updated')

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

