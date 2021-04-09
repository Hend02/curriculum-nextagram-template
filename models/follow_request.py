from models.base_model import BaseModel
import peewee as pw
from models.user import User

class FollowRequest(BaseModel):
    fan_request = pw.ForeignKeyField(User)
    idol_receive = pw.ForeignKeyField(User)
