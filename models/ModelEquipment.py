from .entities.Equipment import Equipment


class ModelEquipment():

    @classmethod
    def getById(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, brand, model, potency FROM equipment WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Equipment(row[0], row[1], row[2], row[3])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def getAllByInstitutionId(self, db, institution_id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT equipment_id FROM institution_equipment WHERE institution_id = {}".format(institution_id)
            cursor.execute(sql)
            records = cursor.fetchall()
            equipments = []
            for row in records:
                eq = self.getById(db, row[0])
                equipments.append(eq)
            return equipments
        except Exception as ex:
            raise Exception(ex)