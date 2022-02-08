from app import db
# from sqlalchemy.dialects.postgresql import JSON
# JSON necessary?


# Example table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User {}>".format(self.username)


# Company table
class Companies(db.Model):
    __tablename__ = "companies"

    company_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    eguide_link = db.Column(db.String(120))
    eguide_image_src = db.Column(db.String(120))
    city = db.Column(db.String(64))
    website = db.Column(db.String(120))
    year = db.Column(db.Integer)
    # Gaat dit goed met arrays?
    discipline = db.Column(db.String(120))
    branch = db.Column(db.String(120))
    tag = db.Column(db.String(120))
    region = db.Column(db.String(64))
    company_size = db.Column(db.String(64))

    def __repr__(self):
        return "<Company ID {}>".format(self.company_id)
