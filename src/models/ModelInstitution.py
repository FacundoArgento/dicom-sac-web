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