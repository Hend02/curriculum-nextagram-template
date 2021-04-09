from models.follow_request import FollowRequest
from models.base_model import BaseModel
import peewee as pw
from models.user import User

class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref='images', on_delete='CASCADE')
    image_url = pw.CharField(null=True)