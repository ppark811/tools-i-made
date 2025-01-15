import os, shutil

source_dir = "./"
destination_dir = "./renamed_files/"

orig_ext = ".txt"
change_ext = ".py"

def copy_and_change_extension(source_dir, destination_dir, orig_ext, change_ext):
    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            if filename.endswith(orig_ext):
                source_path = os.path.join(root, filename)
                relative_path = os.path.relpath(source_path, source_dir)
                destination_path = os.path.join(destination_dir, relative_path)
                
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                
                shutil.copy(source_path, destination_path)
                os.rename(destination_path, os.path.splitext(destination_path)[0] + change_ext)
                
                
copy_and_change_extension(source_dir, destination_dir, orig_ext, change_ext)
