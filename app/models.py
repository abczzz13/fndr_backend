"""Models for the different Tables in DB with additional methods and validation"""
from datetime import datetime
from app import db, jwt
from .utils import get_coordinates
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash


# Pagination mixin Class
class PaginationAPIMixin(object):
    """Class for adding pagination"""

    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs) -> dict:
        """Preparing the output for the GET companies as dictionary with pagination"""
        resources = query.paginate(page, per_page, False)
        data = {
            # Making a dictionary of the query results
            "items": [item.to_dict() for item in resources.items],
            # Meta information about the number of records, pages, etc.
            "_meta": {
                "page": page,
                "per_page": per_page,
                "total_pages": resources.pages,
                "total_items": resources.total,
            },
            # Links to current/next/previous/ pages
            "_links": {
                "self": url_for(endpoint, page=page, per_page=per_page, **kwargs),
                "next": url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                "previous": url_for(endpoint, page=page - 1, per_page=per_page, **kwargs)
                if resources.has_prev
                else None,
            },
        }
        return data


class Users(db.Model):
    """Model for users"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.id}: {self.username} ({self.email})>"

    def set_password(self, password):
        """Set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        """Check password"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        """Return user data as a dictionary"""
        data = {"id": self.id, "username": self.username, "email": self.email}
        return data


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Users.query.filter_by(id=identity).one_or_none()


# Many to Many table for Companies and Meta
companies_meta = db.Table(
    "companies_meta",
    db.Column("company_id", db.Integer, db.ForeignKey("companies.company_id"), index=True),
    db.Column("meta_id", db.Integer, db.ForeignKey("meta.meta_id")),
)


class Companies(PaginationAPIMixin, db.Model):
    """Model for companies"""

    __tablename__ = "companies"

    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64), unique=True, nullable=False)
    logo_image_src = db.Column(db.String(255), default="")
    city_id = db.Column(db.Integer, db.ForeignKey("cities.city_id"), nullable=False)
    website = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)
    company_size = db.Column(db.String(64), nullable=False)
    city = db.relationship("Cities", backref="company", lazy="joined")
    metas = db.relationship(
        "Meta", secondary=companies_meta, lazy="joined", backref=db.backref("meta", lazy="subquery")
    )

    def __repr__(self):
        return f"<Company {self.company_id}: {self.company_name}>"

    def city_name(self):
        """Makes city_name accessible on the object"""
        self.city_name = self.city.city_name

    def to_dict(self) -> dict:
        """Return company as a dictionary"""

        data = {
            "company_id": self.company_id,
            "company_name": self.company_name,
            "logo_image_src": self.logo_image_src,
            "city_name": self.city.city_name,
            "website": self.website,
            "year": self.year,
            "company_size": self.company_size,
            "region": self.city.region,
            "disciplines": [],
            "tags": [],
            "branches": [],
        }
        for meta in self.metas:
            if meta.type == "disciplines":
                data["disciplines"].append(meta.meta_string)
            elif meta.type == "tags":
                data["tags"].append(meta.meta_string)
            elif meta.type == "branches":
                data["branches"].append(meta.meta_string)

        return data


class Cities(db.Model):
    """Models for cities"""

    __tablename__ = "cities"

    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(64), unique=True, nullable=False)
    region = db.Column(db.String(64))
    city_lat = db.Column(db.Float(precision=8))
    city_lng = db.Column(db.Float(precision=8))

    def __repr__(self):
        return f"<City {self.city_id}: {self.city_name} ({self.region})>"

    def get_or_create(self, city_dict) -> int:
        """Returns city if it exists, otherwise creates the new city"""
        query = Cities.query.filter_by(city_name=city_dict["city_name"].title()).first()
        if query is None:
            if "region" not in city_dict:
                city_dict["region"] = "Remote"

            coordinates = get_coordinates(city_dict["city_name"])
            new_city = Cities(
                city_name=city_dict["city_name"].title(),
                region=city_dict["region"],
                city_lat=coordinates["lat"],
                city_lng=coordinates["lng"],
            )

            db.session.add(new_city)
            db.session.commit()

            setattr(self, "city_id", new_city.city_id)

        else:
            setattr(self, "city_id", query.city_id)

        return self.city_id


class Meta(db.Model):
    """Model for meta information"""

    __tablename__ = "meta"

    meta_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
    meta_string = db.Column(db.String(120))

    def __repr__(self):
        return f"<Meta {self.meta_id}: {self.meta_string} ({self.type})>"

    def get_or_create(self, meta_string, meta_type) -> int:
        """Returns meta if it exists, otherwise creates the new meta"""
        query = Meta.query.filter_by(type=meta_type, meta_string=meta_string.title()).first()
        if query is None:
            new_meta = Meta(type=meta_type, meta_string=meta_string.title())
            db.session.add(new_meta)
            db.session.commit()
            setattr(self, "meta_id", new_meta.meta_id)
        else:
            setattr(self, "meta_id", query.meta_id)
        return self.meta_id
