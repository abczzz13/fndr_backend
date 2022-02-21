from app import db, login
from datetime import datetime
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import enum


# Pagination mixin Class
class PaginationAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            # Making a dictionary of the query results
            'items': [item.to_dict() for item in resources.items],
            # Meta information about the number of records, pages, etc.
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            # Links to current/next/previous/ pages
            # TODO: Update urls to include query parameters
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                'previous': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None
            }

        }
        return data


class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}'.format(self.username)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


# Sizes enum for companies.company_size
class Sizes(enum.Enum):
    SMALL = '1-10'
    MEDIUM = '11-50'
    LARGE = '51-100'
    XLARGE = 'GT-100'


# Many to Many table for Companies and Meta
companies_meta = db.Table('companies_meta',
                          db.Column('company_id', db.Integer, db.ForeignKey(
                              'companies.company_id'), index=True),
                          db.Column('meta_id', db.Integer, db.ForeignKey(
                              'meta.meta_id'))
                          )


class Companies(PaginationAPIMixin, db.Model):
    __tablename__ = 'companies'

    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64))
    logo_image_src = db.Column(db.String(255))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'))
    website = db.Column(db.String(255))
    year = db.Column(db.Integer)
    company_size = db.Column(db.Enum(Sizes, values_callable=lambda x: [
                             str(member.value) for member in Sizes]))
    city = db.relationship('Cities', backref='company', lazy='joined')
    metas = db.relationship('Meta', secondary=companies_meta,
                            lazy='dynamic', backref=db.backref('meta', lazy='dynamic'))
    # metas = db.relationship('meta', secondary=companies_meta, back_populates="companies")

    def __repr__(self):
        return '<Company ID: {}>'.format(self.company_id)

    def city_name(self):
        self.city_name = self.city.city_name

    def to_dict(self):
        data = {
            'company_id': self.company_id,
            'company_name': self.company_name,
            'logo_image_src': self.logo_image_src,
            'city_name': self.city.city_name,
            'website': self.website,
            'year': self.year,
            'company_size': self.company_size.value,
            'region': self.city.region.value,
            'disciplines': [],
            'tags': [],
            'branches': []
        }
        # Iterating over all the meta id's to fill the discipline/tags/branches lists
        for meta in self.metas:
            if meta.type.value == "Discipline":
                data['disciplines'].append(meta.meta_string)
            elif meta.type.value == "Tag":
                data['tags'].append(meta.meta_string)
            elif meta.type.value == "Branch":
                data['branches'].append(meta.meta_string)
        return data

    def from_dict(self, data, new_company=False):
        # Add Companies fields
        for field in ["company_name", "logo_image_src", "website", "year", "company_size"]:
            if field in data:
                setattr(self, field, data[field])

        # Check if city is already in Cities table, otherwise add it
        # TODO:
        if "city_name" in data:
            city = Cities.query.filter_by(city_name=data["city_name"]).first()
            if city == 0:
                new_city = Cities(
                    city_name=data["city_name"], region=data["region"])
                self.city.append(new_city)
            # setattr probably wont work because of Cities table?
            else:
                setattr(self, "city_id", city.city_id)
                setattr(self, "city_name", city.city_name)
                setattr(self, "region", city.region)
            # setattr probably wont work because of Cities table?

        # Check if the disciplines, branches, tags already in Meta table, otherwise add it
        # TODO:
        for field in ["disciplines", "branches", "tags"]:
            if field in data:
                # another for loop to iterate over multiple meta_strings?
                for item in data:
                    pass
                # Probably not going to work as the enums is case sensitive
                meta = Meta.query.filter_by(
                    meta_string=data[field], type=field).first()
                if meta == 0:
                    new_meta = Meta(meta_string=data[field], type=field)
                    self.metas.append(new_meta)
                self.metas.append(meta)


# Regions enum for cities.region
class Regions(enum.Enum):
    DR = 'Drenthe'
    FL = 'Flevoland'
    FR = 'Friesland'
    GD = 'Gelderland'
    GR = 'Groningen'
    LB = 'Limburg'
    NB = 'Noord-Brabant'
    NH = 'Noord-Holland'
    OV = 'Overijssel'
    UT = 'Utrecht'
    ZH = 'Zuid-Holland'
    ZL = 'Zeeland'


class Cities(db.Model):
    __tablename__ = 'cities'

    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(64))
    region = db.Column(db.Enum(Regions, values_callable=lambda x: [
                       str(member.value) for member in Regions]))

    def __repr__(self):
        return '<City ID: {}>'.format(self.city_id)


# Types enum for meta.type
# TODO: change to respectively "disciplines", "branches", "tags"
class Types(enum.Enum):
    ONE = 'Discipline'
    TWO = 'Branch'
    THREE = 'Tag'


class Meta(db.Model):
    __tablename__ = 'meta'

    meta_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(Types, values_callable=lambda x: [
        str(member.value) for member in Types]))
    meta_string = db.Column(db.String(120))
    # companies = db.relationship('Companies', secondary = companies_meta, back_populates = "metas")

    def __repr__(self):
        return '<Meta ID {}>'.format(self.meta_id)
