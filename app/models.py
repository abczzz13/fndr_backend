from app import db, login, ma
from datetime import datetime
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import validate, ValidationError, pre_load, post_load

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


# Many to Many table for Companies and Meta
companies_meta = db.Table('companies_meta',
                          db.Column('company_id', db.Integer, db.ForeignKey(
                              'companies.company_id'), index=True),
                          db.Column('meta_id', db.Integer, db.ForeignKey(
                              'meta.meta_id'))
                          )
# TODO: implement ondelete='CASCADE' somewhere...


class Companies(PaginationAPIMixin, db.Model):
    __tablename__ = 'companies'

    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64), unique=True, nullable=False)
    logo_image_src = db.Column(db.String(255), default='')
    city_id = db.Column(db.Integer, db.ForeignKey(
        'cities.city_id'), nullable=False)
    website = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)
    company_size = db.Column(db.String(64), nullable=False)
    city = db.relationship('Cities', backref='company',
                           lazy='joined')
    metas = db.relationship('Meta', secondary=companies_meta,
                            lazy='joined', backref=db.backref('meta', lazy='subquery'))

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
    city_name = db.Column(db.String(64), unique=True, nullable=False)
    region = db.Column(db.String(64))

    def __repr__(self):
        return '<City ID: {}>'.format(self.city_id)


class Meta(db.Model):
    __tablename__ = 'meta'

    meta_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
    meta_string = db.Column(db.String(120))

    def __repr__(self):
        return '<Meta ID {}>'.format(self.meta_id)


class MetaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Meta
        include_fk = True


class CitiesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cities
        include_fk = True

    # city_id = ma.auto_field()
    # city_name = ma.auto_field()
    # region = ma.Str(validate=validate.OneOf(["read", "write", "admin"]))


class CompaniesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Companies
        include_fk = True
        # ordered = True

    company_id = ma.auto_field()
    company_name = ma.auto_field()
    logo_image_src = ma.auto_field()
    city = ma.Pluck(CitiesSchema, 'city_name')
    region = ma.Pluck(CitiesSchema, 'region')
    website = ma.auto_field()
    year = ma.auto_field()
    company_size = ma.auto_field()
    meta = ma.Nested(MetaSchema, attribute='metas',
                     many=True)


class CompaniesValidationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Companies
        include_fk = True

    # List of regions and city_sizes for validation with CompaniesValidationSchema
    regions = ['Remote', 'Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg',
               'Noord-Brabant', 'Noord-Holland', 'Overijssel', 'Utrecht', 'Zuid-Holland', 'Zeeland']
    sizes = ['1-10', '11-50', '51-100', 'GT-100']

    # The Validation fields
    company_name = ma.Str(validate=validate.Length(
        min=2, max=64), required=True)
    logo_image_src = ma.URL()
    city_name = ma.Str(validate=validate.Length(min=2, max=64), required=True)
    region = ma.Str(validate=validate.OneOf(regions))
    website = ma.URL(required=True)
    year = ma.Int(validate=validate.Range(min=1890, max=datetime.now().year))
    company_size = ma.Str(validate=validate.OneOf(
        sizes), required=True)
    disciplines = ma.List(ma.Str(validate=validate.Length(min=2, max=120)))
    branches = ma.List(ma.Str(validate=validate.Length(min=2, max=120)))
    tags = ma.List(ma.Str(validate=validate.Length(min=2, max=120)))

    # Additional Validation checks
    @pre_load
    def unwrap_envelope(self, data, **kwargs):
        if "company_id" in data:
            raise ValidationError(
                "Create new company cannot include company_id. For modifying existing companies please use the PATCH method")
        return data

    @post_load
    def check_company_name(self, data, **kwargs):
        company = Companies.query.filter_by(
            company_name=data['company_name'].title()).first()
        if company is not None:
            raise ValidationError(
                "A company already exists with this company_name. Please use the PATCH method if you would like to modify this company or use a different company_name if you would like to add a different company.")
        return data
