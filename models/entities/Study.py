class Study():

    def __init__(self, id, name, upload_date, user_id, equipment_id, diagnosis_id, contours_verified) -> None:
        self.id = id
        self.name = name
        self.upload_date = upload_date
        self.user_id = user_id
        self.equipment_id = equipment_id
        self.institution_id = diagnosis_id
        self.contours_verified = contours_verified