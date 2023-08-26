from models.ModelStudy import ModelStudy
from payload.DicomLibrary import anonymize_files
import os
from shutil import rmtree
from glob import iglob
from obs import ObsClient

# Config
from config import config

def verify(db, study_name):
    ## verify if study is in Huawei
    record = ModelStudy.getStudyByName(db, study_name)
    if record != None:
        return True
    else:
        return False

def uploadCompleteStudy(institution, operator, tipoEstudio, diagnosis, equipo, uploaded_files, temp_folder, contours_files, study_name):
    try:
        response = False
        save_tmp_folders(uploaded_files, temp_folder, contours_files, study_name)
        anonymize_files(temp_folder)
        upload_folders(institution, operator, tipoEstudio, diagnosis, equipo, temp_folder)
        response = True
    except OSError as err:
        print("OS error: ", err)
        raise
    except Exception as err:
        print("Exception: ", err)
    finally:
        remove_tmp_folders(temp_folder)
        return response


def upload_folders(institution, operator, tipoEstudio, diagnosis, equipo, folder):
    AK = config['development'].AK
    SK = config['development'].SK
    server = config['development'].HUAWEI_SERVER
    bucketName = config['development'].BUCKET_NAME

    # Constructs a obs client instance with your account for accessing OBS
    obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=server)
    
    folderpath = folder
    recursive_path = folderpath + "/**"

    save_folder = institution.name
    
    try: 
        for filename in iglob(recursive_path, recursive=True):
            objectKey = save_folder + filename
            objectKey = objectKey.replace("tmp/", "/")
            if os.path.isfile(filename):
                resp = obsClient.putFile(bucketName=bucketName, objectKey=objectKey, file_path=filename)
                if resp.status < 300: 
                    print('requestId:', resp.requestId) 
                    print('uploaded Filename:', objectKey)
                else: 
                    print('errorCode:', resp.errorCode) 
                    print('errorMessage:', resp.errorMessage)
                    break
    except:
        import traceback
        print(traceback.format_exc())
    finally:
        obsClient.close()

def save_tmp_folders(uploaded_files, dest_folder, contours, study_name):
    for file in uploaded_files:
        savefiles(file, dest_folder)
    # contours
    if not contours or not any(f for f in contours):
        pass
    else:
        study_folder = os.path.join(dest_folder, study_name)
        for file in contours:
            savefiles(file, study_folder)

def savefiles(file, dest_folder):
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
