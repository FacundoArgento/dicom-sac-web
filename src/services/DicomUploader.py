from payload.DicomLibrary import anonymize_files
import os
from shutil import rmtree

def uploadCompleteStudy(institutionName, operator, tipoEstudio, tipoDiagnostico, equipo, uploaded_files, temp_folder):
    try:
        save_tmp_folders(uploaded_files, temp_folder)
        anonymize_files(temp_folder)
        #upload_folders()
        remove_tmp_folders(temp_folder)        
    except OSError as err:
        print("OS error: ", err)
        raise
    except Exception as err:
        print("Exception: ", err)


def upload_folders():
    print("to be implemented")

def save_tmp_folders(uploaded_files, dest_folder):
    for file in uploaded_files:
        file_path = os.path.join(dest_folder, file.filename)
        dirname = os.path.dirname(file_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        open(file_path, "a").close()
        file.save(file_path)

def remove_tmp_folders(directory_path):
    with os.scandir(directory_path) as entries:
       for entry in entries:
         if entry.is_file():
            os.unlink(entry.path)
         else:
            rmtree(entry.path)
    print("All files deleted successfully.")
