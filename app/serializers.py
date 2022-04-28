from datetime import datetime

from app import ma
from marshmallow import validate, ValidationError, pre_load, post_load

from .models import Companies, Users


class NewAdminSchema(ma.SQLAlchemySchema):
    """Validation Schema for users/admins"""

    class Meta:
        """Meta information"""

        model = Users
        include_fk = True

    # The Validation Field:
    username = ma.Str(validate=validate.Length(min=2, max=64), required=True)
    email = ma.Email(validate=validate.Length(min=2, max=64), required=True)
    password = ma.Str(validate=validate.Length(min=8, max=64), required=True, load_only=True)

    # Additional Validation checks
    @post_load
    def username_exists(self, data, **kwargs):
        """Lookup if username already exists"""
        if Users.query.filter(Users.username == data["username"]).one_or_none():
            raise ValidationError("This username is already in use, please use a different username.")
        return data

    @post_load
    def email_exists(self, data, **kwargs):
        """Lookup if email already exists"""
        if Users.query.filter(Users.email == data["email"]).one_or_none():
            raise ValidationError("This email address is already in use, please use a different email address.")
        return data


class CompaniesValidationSchema(ma.SQLAlchemySchema):
    """Validation Schema for POST company"""

    class Meta:
        """Meta information"""

        model = Companies
        include_fk = True

    # List of regions and city_sizes for validation with CompaniesValidationSchema
    regions = [
        "Remote",
        "Drenthe",
        "Flevoland",
        "Friesland",
        "Gelderland",
        "Groningen",
        "Limburg",
        "Noord-Brabant",
        "Noord-Holland",
        "Overijssel",
        "Utrecht",
        "Zuid-Holland",
        "Zeeland",
    ]
    sizes = ["1-10", "11-50", "51-100", "GT-100"]

    # The Validation fields
    company_name = ma.Str(validate=validate.Length(min=2, max=64), required=True)
    logo_image_src = ma.URL()
    city_name = ma.Str(validate=validate.Length(min=2, max=64), required=True)
    region = ma.Str(validate=validate.OneOf(regions))
    website = ma.URL(required=True)
    year = ma.Int(validate=validate.Range(min=1890, max=datetime.now().year))
    company_size = ma.Str(validate=validate.OneOf(sizes), required=True)
    disciplines = ma.List(ma.Str(validate=validate.Length(min=2, max=120)))
    branches = ma.List(ma.Str(validate=validate.Length(min=2, max=120)))
    tags = ma.List(ma.Str(validate=validate.Length(min=2, max=120)))

    # Additional Validation checks
    @pre_load
    def company_id_exists(self, data, **kwargs):
        """Validate there is not company_id in data"""
        if "company_id" in data:
            raise ValidationError(
                "Create new company cannot include company_id. For modifying existing companies please use the PATCH method"
            )
        return data

    @post_load
    def company_name_exists(self, data, **kwargs):
        """Lookup if company_name already exists"""
        if Companies.query.filter(Companies.company_name == data["company_name"].title()).one_or_none():
            raise ValidationError(
                "A company already exists with this company_name. Please use the PATCH method if you would like to modify this company or use a different company_name if you would like to add a different company."
            )
        return data


class CompaniesPatchSchema(ma.SQLAlchemySchema):
    """Validation Schema for PATCH company"""

    class Meta:
        """Meta information"""

        model = Companies
        include_fk = True

    # List of regions and city_sizes for validation with CompaniesValidationSchema
    regions = [
        "Remote",
        "Drenthe",
        "Flevoland",
        "Friesland",
        "Gelderland",
        "Groningen",
        "Limburg",
        "Noord-Brabant",
        "Noord-Holland",
        "Overijssel",
        "Utrecht",
        "Zuid-Holland",
        "Zeeland",
    ]
    sizes = ["1-10", "11-50", "51-100", "GT-100"]

    # The Validation fields
    company_name = ma.Str(validate=validate.Length(min=2, max=64), required=True)
    logo_image_src = ma.URL()
    city_name = ma.Str(validate=validate.Length(min=2, max=64), required=True)
    region = ma.Str(validate=validate.OneOf(regions), dump_only=True)
    website = ma.URL(required=True)
    year = ma.Int(validate=validate.Range(min=1890, max=datetime.now().year))
    company_size = ma.Str(validate=validate.OneOf(sizes), required=True)
    disciplines = ma.List(ma.Str(validate=validate.Length(min=2, max=120)))
    branches = ma.List(ma.Str(validate=validate.Length(min=2, max=120)))
    tags = ma.List(ma.Str(validate=validate.Length(min=2, max=120)))
    id_for_check_company = ma.Int()

    # Additional Validation check
    @post_load
    def company_name_exists(self, data, **kwargs):
        """Lookup if company_name already exists"""
        if "company_name" in data:
            company = Companies.query.filter_by(company_name=data["company_name"].title()).first()
            if company is not None and company.company_id != data["id_for_check_company"]:
                raise ValidationError(
                    "A company already exists with this company_name. Please use a different company_name."
                )
            return data
        return data
