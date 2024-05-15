import os
import unittest
import sys
sys.path.append('..')


class TestLogin(unittest.TestCase):
    """The unit tests for login feature"""

    def test_valid_customer_login(self) -> None:
        """The unit test to check valid customer login"""

        from monash_merchant.model.user import User
        from monash_merchant.model.user import Customer

        valid_user = User.login(
            email='member@student.monash.edu',
            password='Monash1234',
            data_path=os.path.join('..', 'data'))

        self.assertIsInstance(valid_user, Customer)

    def test_valid_admin_login(self) -> None:
        """The unit test to check valid administrator login"""

        from monash_merchant.model.user import User
        from monash_merchant.model.user import Administrator

        valid_user = User.login(
            email='admin@merchant.monash.edu',
            password='12345678',
            data_path=os.path.join('..', 'data'))

        self.assertIsInstance(valid_user, Administrator)

    def test_invalid_user_login(self) -> None:
        """The unit test to check invalid login"""

        from monash_merchant.model.user import User

        valid_user = User.login(
            email='this.user@does.not.exist',
            password='anything',
            data_path=os.path.join('..', 'data'))

        self.assertIsNone(valid_user)


if __name__ == '__main__':
    unittest.main()
