from .entities.Diagnosis import Diagnosis


class ModelDiagnosis():


    @classmethod
    def getAllDiagnosis(self, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT * FROM diagnosis ORDER BY name"
            cursor.execute(sql)
            records = cursor.fetchall()
            all_diagnosis = []
            for row in records:
                d = Diagnosis(row[0], row[1])   
                all_diagnosis.append(d)
            return all_diagnosis
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def getById(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, name FROM diagnosis WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Diagnosis(row[0], row[1])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)