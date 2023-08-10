from payload.DicomLibrary import anonymize_files
from os import path
import os


def uploadCompleteStudy(institutionName, operator, tipoEstudio, tipoDiagnostico, equipo, uploaded_files, upload_folder):
    # first anonimize files
    for file in uploaded_files:
        file_path=os.path.join(upload_folder, file.filename)
        if not os.path.exists(file_path):
            print(file_path)
            # if the demo_folder directory is not present 
            # then create it.
            os.makedirs(file_path)
        open(file_path, "a").close()
        print("FILENMAME CREATED")
        file.save(path.join(upload_folder, file_path))
        
