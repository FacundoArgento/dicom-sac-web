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
            cursor.execute("SELECT * FROM study WHERE name = '%s'" % studyname)
            row = cursor.fetchone()
            if row != None:
                return Study(row[0], row[1] ,row[2], row[3], row[4], row[5], row[6])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def getAllStudyForRevision(self, db):
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT *
                FROM study
                WHERE contours_verified = 0
                """
            cursor.execute(sql)
            records = cursor.fetchall()
            studys = []
            for row in records:
                study = Study(row[0], row[1] ,row[2], row[3], row[4], row[5], row[6])
                studys.append(study)
            return studys
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def enableStudyContoursById(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = """
                UPDATE study
                SET contours_verified = 1
                WHERE id={}
            """.format(id)
            cursor.execute(sql)
            db.connection.commit()
            cursor.close()
        except Exception as ex:
            raise Exception(ex)