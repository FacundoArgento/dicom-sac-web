class Study():

    def __init__(self, id, name, upload_date, user_id="", equipment_id="", institution_id="") -> None:
        self.id = id
        self.name = name
        self.upload_date = upload_date
        self.user_id = user_id
        self.equipment_id = equipment_id
        self.institution_id = institution_id