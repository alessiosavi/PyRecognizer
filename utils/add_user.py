"""Create a new admin user able to view the /reports endpoint."""
from getpass import getpass
import sys

from flask import current_app


def main():
    """Main entry point for script."""
    with app.app_context():
        db.metadata.create_all(db.engine)
        print('Enter email address: ')
        email = input()
        password = getpass()
        assert password == getpass('Password (again):')

        user = User(
            email=email,
            password=bcrypt.generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print('User added.')


if __name__ == '__main__':
    sys.exit(main())
