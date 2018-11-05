import mongoengine
from datetime import datetime

import remanager_back.database.mongo_digiall_utils as mongo_utils


class UserExtra(mongoengine.Document):
    fechaAlta = mongoengine.DateTimeField(default=datetime.now)

    login = mongoengine.StringField(unique=True)

    profilePictureUrl = mongoengine.StringField()

    picturesUrls = mongoengine.ListField(mongoengine.StringField(), default=[])

    def to_dict(self):
        return mongo_utils.mongo_to_dict_1(self)

    meta = {
        'db_alias': 'core',
        'collection': 'user_extra'
    }
