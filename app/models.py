from datetime import datetime
from app import db, ma, jwt
from .utils import get_coordinates
from flask import url_for
from marshmallow import validate, ValidationError, pre_load, post_load
from werkzeug.security import generate_password_hash, check_password_hash


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


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(64),
        index=True,
        unique=True,
        nullable=False)
    email = db.Column(
        db.String(128),
        index=True,
        unique=True,
        nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.id}: {self.username} ({self.email})>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
        return data


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Users.query.filter_by(id=identity).one_or_none()


# Many to Many table for Companies and Meta
companies_meta = db.Table('companies_meta',
                          db.Column('company_id',
                                    db.Integer,
                                    db.ForeignKey('companies.company_id'),
                                    index=True),
                          db.Column('meta_id',
                                    db.Integer,
                                    db.ForeignKey('meta.meta_id')))


class Companies(PaginationAPIMixin, db.Model):
    __tablename__ = 'companies'

    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(
        db.String(64),
        unique=True,
        nullable=False)
    logo_image_src = db.Column(db.String(255), default='')
    city_id = db.Column(
        db.Integer,
        db.ForeignKey('cities.city_id'),
        nullable=False)
    website = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)
    company_size = db.Column(db.String(64), nullable=False)
    city = db.relationship('Cities',
                           backref='company',
                           lazy='joined')
    metas = db.relationship('Meta',
                            secondary=companies_meta,
                            lazy='joined',
                            backref=db.backref('meta', lazy='subquery'))

    def __repr__(self):
        return f'<Company {self.company_id}: {self.company_name}>'

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
            'company_size': self.company_size,
            'region': self.city.region,
            'disciplines': [],
            'tags': [],
            'branches': []
        }
        for meta in self.metas:
            if meta.type == 'disciplines':
                data['disciplines'].append(meta.meta_string)
            elif meta.type == 'tags':
                data['tags'].append(meta.meta_string)
            elif meta.type == 'branches':
                data['branches'].append(meta.meta_string)

        return data


class Cities(db.Model):
    __tablename__ = 'cities'

    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(
        db.String(64),
        unique=True,
        nullable=False)
    region = db.Column(db.String(64))
    city_lat = db.Column(db.Float(precision=8))
    city_lng = db.Column(db.Float(precision=8))

    def __repr__(self):
        return f'<City {self.city_id}: {self.city_name} ({self.region})>'

    def get_or_create(self, dict):
        query = Cities.query.filter_by(
            city_name=dict['city_name'].title()).first()
        if query is None:
            if 'region' not in dict:
                dict['region'] = 'Remote'

            coordinates = get_coordinates(dict['city_name'])
            new_city = Cities(
                city_name=dict['city_name'].title(),
                region=dict['region'],
                city_lat=coordinates['lat'],
                city_lng=coordinates['lng'])

            db.session.add(new_city)
            db.session.commit()

            setattr(self, 'city_id', new_city.city_id)

        else:
            setattr(self, 'city_id', query.city_id)

        return self.city_id


class Meta(db.Model):
    __tablename__ = 'meta'

    meta_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
    meta_string = db.Column(db.String(120))

    def __repr__(self):
        return f'<Meta {self.meta_id}: {self.meta_string} ({self.type})>'

    def get_or_create(self, meta_string, type):
        query = Meta.query.filter_by(
            type=type, meta_string=meta_string).first()
        if query is None:
            new_meta = Meta(type=type, meta_string=meta_string)
            db.session.add(new_meta)
            db.session.commit()
            setattr(self, 'meta_id', new_meta.meta_id)
        else:
            setattr(self, 'meta_id', query.meta_id)
        return self.meta_id


class NewAdminSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Users
        include_fk = True

    # The Validation Field:
    username = ma.Str(
        validate=validate.Length(min=2, max=64),
        required=True)
    email = ma.Email(
        validate=validate.Length(min=2, max=64),
        required=True)
    password = ma.Str(
        validate=validate.Length(min=8, max=64),
        required=True,
        load_only=True)

    # Additional Validation checks
    @post_load
    def username_exists(self, data, **kwargs):
        if Users.query.filter(Users.username == data['username']).one_or_none():
            raise ValidationError(
                "This username is already in use, please use a different username.")
        return data

    @post_load
    def email_exists(self, data, **kwargs):
        if Users.query.filter(Users.email == data['email']).one_or_none():
            raise ValidationError(
                "This email address is already in use, please use a different email address.")
        return data


class CompaniesValidationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Companies
        include_fk = True

    # List of regions and city_sizes for validation with CompaniesValidationSchema
    regions = ['Remote', 'Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg',
               'Noord-Brabant', 'Noord-Holland', 'Overijssel', 'Utrecht', 'Zuid-Holland', 'Zeeland']
    sizes = ['1-10', '11-50', '51-100', 'GT-100']

    # The Validation fields
    company_name = ma.Str(
        validate=validate.Length(min=2, max=64),
        required=True)
    logo_image_src = ma.URL()
    city_name = ma.Str(
        validate=validate.Length(min=2, max=64),
        required=True)
    region = ma.Str(validate=validate.OneOf(regions))
    website = ma.URL(required=True)
    year = ma.Int(
        validate=validate.Range(min=1890, max=datetime.now().year))
    company_size = ma.Str(
        validate=validate.OneOf(sizes),
        required=True)
    disciplines = ma.List(ma.Str(validate=validate.Length(min=2, max=120)))
    branches = ma.List(ma.Str(validate=validate.Length(min=2, max=120)))
    tags = ma.List(ma.Str(validate=validate.Length(min=2, max=120)))

    # Additional Validation checks
    @pre_load
    def company_id_exists(self, data, **kwargs):
        if "company_id" in data:
            raise ValidationError(
                "Create new company cannot include company_id. For modifying existing companies please use the PATCH method")
        return data

    @post_load
    def company_name_exists(self, data, **kwargs):
        if Companies.query.filter(Companies.company_name == data['company_name'].title()).one_or_none():
            raise ValidationError(
                "A company already exists with this company_name. Please use the PATCH method if you would like to modify this company or use a different company_name if you would like to add a different company.")
        return data


class CompaniesPatchSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Companies
        include_fk = True

    # List of regions and city_sizes for validation with CompaniesValidationSchema
    regions = ['Remote', 'Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg',
               'Noord-Brabant', 'Noord-Holland', 'Overijssel', 'Utrecht', 'Zuid-Holland', 'Zeeland']
    sizes = ['1-10', '11-50', '51-100', 'GT-100']

    # The Validation fields
    company_name = ma.Str(
        validate=validate.Length(min=2, max=64),
        required=True)
    logo_image_src = ma.URL()
    city_name = ma.Str(
        validate=validate.Length(min=2, max=64),
        required=True)
    region = ma.Str(
        validate=validate.OneOf(regions),
        dump_only=True)
    website = ma.URL(required=True)
    year = ma.Int(
        validate=validate.Range(min=1890, max=datetime.now().year))
    company_size = ma.Str(validate=validate.OneOf(
        sizes), required=True)
    disciplines = ma.List(
        ma.Str(validate=validate.Length(min=2, max=120)))
    branches = ma.List(ma.Str(validate=validate.Length(min=2, max=120)))
    tags = ma.List(ma.Str(validate=validate.Length(min=2, max=120)))
    id_for_check_company = ma.Int()

    # Additional Validation check
    @post_load
    def company_name_exists(self, data, **kwargs):
        if 'company_name' in data:
            company = Companies.query.filter_by(
                company_name=data['company_name'].title()).first()
            if company is not None and company.company_id != data['id_for_check_company']:
                raise ValidationError(
                    "A company already exists with this company_name. Please use a different company_name.")
            return data
        return data
