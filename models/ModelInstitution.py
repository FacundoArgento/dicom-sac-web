from .entities.Institution import Institution


class ModelInstitution():

    @classmethod
    def getAllInstitutions(self, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT * FROM institution"
            cursor.execute(sql)
            records = cursor.fetchall()
            institutions = []
            for row in records:
                inst = Institution(row[0], row[1])   
                institutions.append(inst)
            return institutions
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def getById(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, name FROM institution WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Institution(row[0], row[1])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def getAllByUserId(self, db, user_id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT institution_id FROM user_institutions WHERE user_id = {}".format(user_id)
            cursor.execute(sql)
            records = cursor.fetchall()
            institutions = []
            for row in records:
                institution = self.getById(db, row[0])
                institutions.append(institution)
            return institutions
        except Exception as ex:
            raise Exception(ex)