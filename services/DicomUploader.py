from models.ModelStudy import ModelStudy
from payload.DicomLibrary import anonymize_files
import os
from shutil import rmtree
from glob import iglob
from obs import ObsClient

# Config
from config import config

def uploadCompleteStudy(institution, operator, tipoEstudio, diagnosis, equipo, temp_folder, contour_file, study_name):
    try:
        response = False
        actual_study_name = os.listdir(temp_folder)[0]
        save_contour(temp_folder, contour_file, actual_study_name)
        anonymize_files(temp_folder)
        encoded_study_name = renameStudyTmpFolder(temp_folder, actual_study_name, study_name)
        upload_folders(institution, operator, tipoEstudio, diagnosis, equipo, temp_folder)
        response = True
    except OSError as err:
        print("OS error: ", err)
        raise
    except Exception as err:
        print("Exception: ", err)
    finally:
        remove_tmp_folders(temp_folder, encoded_study_name)
        return response


def upload_folders(institution, operator, tipoEstudio, diagnosis, equipo, folder):
    AK = config['deployConfig'].AK
    SK = config['deployConfig'].SK
    server = config['deployConfig'].HUAWEI_SERVER
    bucketName = config['deployConfig'].BUCKET_NAME

    # Constructs a obs client instance with your account for accessing OBS
    obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=server)
    metadata={'institution':institution, 'operador':operator, 'tipoStudio':tipoEstudio, 'diagnostico':diagnosis, 'equipo':equipo}
    folderpath = folder
    recursive_path = folderpath + "/**"

    save_folder = institution.name
    i=0
    try: 
        for filename in iglob(recursive_path, recursive=True):
            objectKey = save_folder + filename
            objectKey = objectKey.replace("tmp/", "/")
            if os.path.isfile(filename):
                resp = obsClient.putFile(bucketName=bucketName, objectKey=objectKey, file_path=filename, metadata=metadata)
                if resp.status < 300: 
                    print('uploaded Filename:', objectKey)
                else: 
                    print('errorCode:', resp.errorCode) 
                    print('errorMessage:', resp.errorMessage)
                    break
            i+=1
    except:
        import traceback
        print(traceback.format_exc())
    finally:
        print(f"cantidad de archivos subidos: {i}")
        obsClient.close()

def save_contour(dest_folder, contour_file, study_name):
    if not contour_file:
        pass
    else:
        study_folder = os.path.join(dest_folder, study_name)
        savefiles(contour_file, study_folder)
        renameContoursFile(contour_file, study_folder)

def save_tmp_folders(uploaded_files, dest_folder):
    for file in uploaded_files:
        savefiles(file, dest_folder)

def savefiles(file, dest_folder):
    file_path = os.path.join(dest_folder, file.filename)
    dirname = os.path.dirname(file_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    open(file_path, "a").close()
    file.save(file_path)


def remove_tmp_folders(directory_path, encoded_study_name):
    path = directory_path + "/" + encoded_study_name
    with os.scandir(path) as entries:
       for entry in entries:
         if entry.is_file():
            os.unlink(entry.path)
         else:
            rmtree(entry.path)
    os.rmdir(path)  # finnaly remove dir.
    print("All files deleted successfully.")

def renameStudyTmpFolder(temp_folder, actual_study_name, studyName):
    encoded_name = studyName.encode('ascii', 'ignore').decode('ascii')
    os.rename(temp_folder + "/" + actual_study_name, temp_folder + "/" + encoded_name)
    return encoded_name

def renameContoursFile(file, dest_folder):
    contour_path = os.path.join(dest_folder, file.filename)
    if os.path.isdir(contour_path):
        return
    file_extension = os.path.splitext(file.filename)[1]
    os.rename(contour_path, os.path.join(dest_folder, "contours" + file_extension))