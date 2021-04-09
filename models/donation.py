from models.base_model import BaseModel
import peewee as pw
from models.image import Image
from models.user import User

class Donation(BaseModel):
    image = pw.ForeignKeyField(Image, backref='donations', on_delete='CASCADE')
    user = pw.ForeignKeyField(User, backref='donations', on_delete='CASCADE')
    amount = pw.DecimalField(default=0,null=False)