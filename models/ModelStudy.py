from .entities.Study import Study
import datetime


class ModelStudy():

    @classmethod
    def uploadStudy(self, db, study_name, current_user, equipment, diagnosis):
        try:
            cursor = db.connection.cursor()
            query = """ INSERT INTO study (name, upload_date, user_id, equipment_id, diagnosis_id) VALUES (%s, %s, %s, %s, %s) """
            record = (study_name, datetime.datetime.now(), current_user.id, equipment.id, diagnosis.id)
            cursor.execute(query, record)
            db.connection.commit()
            cursor.close()
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def getStudyByName(self, db, studyname):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT id, name, upload_date FROM study WHERE name = '%s'" % studyname)
            row = cursor.fetchone()
            if row != None:
                return Study(row[0], row[1], row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)