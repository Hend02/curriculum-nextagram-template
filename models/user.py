from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from playhouse.hybrid import hybrid_property
import re


class User(BaseModel, UserMixin):
    name = pw.CharField(unique=False, null=False)
    email = pw.CharField(unique=True, null=False)
    hash_password = pw.CharField(unique=False, null=True)
    password = None
    profile_image = pw.CharField(unique=False, default="https://www.tenforums.com/geek/gars/images/2/types/thumb_15951118880user.png")
    is_private = pw.BooleanField(default=False)

    def validate(self):
        duplicate_name = User.get_or_none(User.name == self.name)

        if duplicate_name == None:
            print("Username is NoneType")
        # elif duplicate_name:
        #     self.errors.append('Username is not unique')

        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_email == None:
            print("Email is NoneType") 
        elif duplicate_email.id != self.id:
            self.errors.append('Email is not unique')
        
        if self.password == None:
            print("Password is Nonetype")
        elif len(self.password) <= 6:
            self.errors.append("Password must contain more than 6 characters.")
        elif len(self.password) > 6:
            has_lower = re.search(r"[a-z]", self.password)
            has_upper = re.search(r"[A-Z]", self.password)
            has_special = re.search(r"[\W]", self.password)

            if has_lower and has_upper and has_special:
                self.hash_password = generate_password_hash(self.password)
            else:
                self.errors.append("Password must contain atleast one lower, upper, and special character.")

        if self.profile_image == None:
            print("Profile Image is None")



