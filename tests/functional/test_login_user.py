from app.models import Users
from flask_login import current_user


def test_login_user(client, init_testdb, new_user, login_users):
    """
    GIVEN that there is a Test user registered and stored in the DB
    WHEN the user is logged in
    THEN the query for the Test user will contain valid user credentials and the user is currently logged in
    """

    username = "Test User"
    password = "testtest"

    user = Users.query.filter_by(username=username).first()

    assert user.username == username
    assert user.check_password(password)
    assert current_user.is_authenticated
    assert user.last_seen is not None
