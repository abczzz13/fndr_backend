"""Module to start the import of the .json database file into the DB"""
import os
from app import create_app
from app.utils_import import import_data, create_admin
from config import Config


def main():

    while True:
        answer = input(
            "Are you sure you want to import the .json file into the DB and create an admin user? (Y/N) "
        ).lower()

        if answer in ["yes", "y"]:
            print("The import has started...")
            app = create_app(config_class=os.environ.get("APP_SETTINGS"))
            app.app_context().push()

            file = os.path.join(Config.APP_ROOT, "app", "db_v2.json")
            import_data(file)
            create_admin()
            print("The import has been completed")

        elif answer in ["no", "n"]:
            break


if __name__ == "__main__":
    main()
