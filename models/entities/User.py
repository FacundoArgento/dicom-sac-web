from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, username, password, active=True, operator_name="", instutution_id=0) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.active = active
        self.operator_name = operator_name
        self.institution_id = instutution_id

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)