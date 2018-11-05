from remanager_back.data_auth import db
from passlib.hash import pbkdf2_sha256 as sha256


user_authorities = db.Table('user_authorities',
                            db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                            db.Column('authority_id', db.Integer, db.ForeignKey('authority.id')))


class AuthorityModel(db.Model):
    __tablename__ = 'authority'

    id = db.Column(db.Integer, primary_key=True)
    authority_name = db.Column(db.String(20))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_authority_name(cls, authority_name):
        return cls.query.filter_by(authority_name=authority_name).first()

    @classmethod
    def return_all(cls):
        return [authority.authority_name for authority in AuthorityModel.query.all()]


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    firstName = db.Column(db.String())
    lastName = db.Column(db.String())
    email = db.Column(db.String(), unique=True, nullable=False)
    activated = db.Column(db.Boolean())
    organizationId = db.Column(db.String())

    authorities = db.relationship('AuthorityModel', secondary=user_authorities,
                                  backref=db.backref('users', lazy='dynamic'))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_me(self):
        db.session.delete(self)
        db.session.commit()

    def has_authority(self, authority_string: str) -> bool:
        if authority_string not in [authority.authority_name for authority in self.authorities]:
            return False
        return True

    def to_json(self):
        return {
            'id': self.id,
            'login': self.login,
            'password': self.password,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'activated': self.activated,
            'organizationId': self.organizationId,
            'authorities': [authority.authority_name for authority in self.authorities]
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_login(cls, login):
        return cls.query.filter_by(login=login).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_organization_id(cls, organization_id):
        return cls.query.filter_by(organizationId=organization_id)

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'id': x.id,
                'login': x.login,
                'password': x.password,
                'firstName': x.firstName,
                'lastName': x.lastName,
                'email': x.email,
                'activated': x.activated,
                'organizationId': x.organizationId,
                'authorities': [authority.authority_name for authority in x.authorities]
            }
        return list(map(lambda x: to_json(x), UserModel.query.all()))

    # @classmethod
    # def delete_all(cls):
    #     try:
    #         num_rows_deleted = db.session.query(cls).delete()
    #         db.session.commit()
    #         return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
    #     except:
    #         return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hashed_password):
        return sha256.verify(password, hashed_password)


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
