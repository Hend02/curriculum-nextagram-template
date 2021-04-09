from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property

class Follow(BaseModel):
    fan = pw.ForeignKeyField(User, on_delete='CASCADE')
    idol = pw.ForeignKeyField(User, on_delete='CASCADE')

    @hybrid_property
    def fans(self):
        return User.select().join(Follow, on=(User.id==Follow.fan)).where(Follow.idol == self)