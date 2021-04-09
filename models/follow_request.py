from models.base_model import BaseModel
import peewee as pw
from models.user import User

class FollowRequest(BaseModel):
    fan_request = pw.ForeignKeyField(User, on_delete='CASCADE')
    idol_receive = pw.ForeignKeyField(User, on_delete='CASCADE')
