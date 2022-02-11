from flask_seeder import Seeder, Faker, generator
# from app.models import Cities, Companies, Meta, companies_meta

# SQLAlchemy database model:


class Cities(Base):
    def __init__(self, city_id=None, city_name=None, region=None):
        self.city_id = city_id
        self.city_name = city_name
        self.region = region

    def __str__(self):
        return "ID=%d, Name=%s, Region=%d" % (self.city_id, self.city_name, self.region)


# All seeders inherit from Seeder
class DemoSeeder(Seeder):

    # run() will be called by Flask-Seeder
    def run(self):
        # Create a new Faker and tell it how to create User objects
        faker = Faker(
            cls=...,
            init={
                "city_id": generator.Sequence(),
                "city_name": generator.Name(),
                "region": "Zuid-Holland"
            }
        )

        # Create 50 cities
        for city in faker.create(50):
            print(f"Adding user: {city}")
            self.db.session.add(city)
