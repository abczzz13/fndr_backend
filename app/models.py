from app import db
import enum

# TODO: find out if db.relationship is warranted


# Sizes enum for companies.company_size
class Sizes(enum.Enum):
    SMALL = "1-10"
    MEDIUM = "11-50"
    LARGE = "51-100"
    XLARGE = "GT-100"


class Companies(db.Model):
    __tablename__ = "companies"

    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64))
    logo_image_src = db.Column(db.String(255))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'))
    website = db.Column(db.String(255))
    year = db.Column(db.Integer)
    company_size = db.Column(db.Enum(Sizes, values_callable=lambda x: [
                             str(member.value) for member in Sizes]))
    meta = db.relationship('Meta', backref='company', lazy='dynamic')

    def __repr__(self):
        return "<Company ID {}>".format(self.company_id)


# Regions enum for cities.region
class Regions(enum.Enum):
    DR = "Drenthe"
    FL = "Flevoland"
    FR = "Friesland"
    GD = "Gelderland"
    GR = "Groningen"
    LB = "Limburg"
    NB = "Noord-Brabant"
    NH = "Noord-Holland"
    OV = "Overijssel"
    UT = "Utrecht"
    ZH = "Zuid-Holland"
    ZL = "Zeeland"


class Cities(db.Model):
    __tablename__ = "cities"

    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(64))
    region = db.Column(db.Enum(Regions, values_callable=lambda x: [
                       str(member.value) for member in Regions]))
    company = db.relationship('Companies', backref='city', lazy='dynamic')

    def __repr__(self):
        return "<City ID {}>".format(self.city_id)


# Types enum for meta.type
class Types(enum.Enum):
    ONE = "Discipline"
    TWO = "Branch"
    THREE = "Tag"


class Meta(db.Model):
    __tablename__ = "meta"

    meta_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(Types, values_callable=lambda x: [
        str(member.value) for member in Types]))
    meta_string = db.Column(db.String(120))

    def __repr__(self):
        return "<Meta ID {}>".format(self.meta_id)


# Many to Many table for Companies and Meta
companies_meta = db.Table('companies_meta',
                          db.Column('meta_id', db.Integer, db.ForeignKey(
                              'meta.meta_id'), primary_key=True),
                          db.Column('company_id', db.Integer, db.ForeignKey(
                              'companies.company_id'), primary_key=True)
                          )
