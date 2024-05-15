from __future__ import annotations

from enum import Enum

from util.csv_table import CsvTable


class UserRole(Enum):
    Customer = 'customer'
    Administrator = 'administrator'


class User(object):
    """This class represents the parent class of user which contains common user functions"""

    def __init__(self, user_id: str, role: UserRole, email: str, password: str) -> None:
        """
        The __init__ method for User.
        :param user_id: UserId for the user. Expected to be unique. Use as table key.
        :param role: Either customer or administrator.
        :param email: Email to be used for login.
        :param password: Password to be used for login.
        """
        self.user_id = user_id
        self.role = role
        self.email = email
        self.password = password

    @staticmethod
    def login(email: str, password: str, data_path: str = 'data') -> Customer | Administrator | None:
        """
        The login method used to log into the system.
        :param email: The email to lookup.
        :param password: The password to lookup.
        :param data_path: The path to the users.csv file containing login data.
        :return: If successful a Customer() or Administrator() object, otherwise None.
        """
        users_table = CsvTable(
            name='users',
            column_names=['user_id', 'role', 'email', 'password'],
            data_path=data_path
        )
        users = users_table.select(
            where={'email': email,
                   'password': password}
        )

        if len(users) == 0:
            return None
        else:
            user = users[0]

        if user['role'] == UserRole.Customer.value:
            return Customer(
                user_id=user['user_id'],
                email=user['email'],
                password=user['password'],
                data_path=data_path
            )
        elif user['role'] == UserRole.Administrator.value:
            return Administrator(
                user_id=user['user_id'],
                email=user['email'],
                password=user['password']
            )
        else:
            error = f'User role {user["role"]} is not valid.'
            raise ValueError(error)


class Customer(User):
    """This class contains the subclass for customer derived from User"""

    def __init__(self, user_id: str, email: str, password: str, data_path: str | None = 'data') -> None:
        """
        The __init__ method for Customer.
        :param user_id: UserId for the user. Expected to be unique. Use as table key.
        :param email: email to be used for login.
        :param password: Password to be used for login.
        :param data_path: The path to the users.csv file containing login data.
        """
        super().__init__(
            user_id=user_id,
            role=UserRole.Customer,
            email=email,
            password=password
        )
        customer_table = CsvTable(
            name='customer',
            column_names=['user_id', 'first_name', 'last_name', 'date_of_birth',
                          'gender', 'mobile_number', 'address', 'fund', 'membership'],
            data_path=data_path
        )
        customers = customer_table.select(
            where={'user_id': user_id}
        )

        customer = customers[0] if customers else None

        self.first_name = customer['first_name'] if customer else ''
        self.last_name = customer['last_name'] if customer else ''
        self.date_of_birth = customer['date_of_birth'] if customer else ''
        self.gender = customer['gender'] if customer else ''
        self.mobile_number = customer['mobile_number'] if customer else ''
        self.address = customer['address'] if customer else ''
        self.fund = customer['fund'] if customer else ''
        self.membership = customer['membership'] if customer else ''


class Administrator(User):
    """This class contains the subclass for customer derived from Administrator"""

    def __init__(self, user_id: str, email: str, password: str) -> None:
        """
        The __init__ method for Administrator.
        :param user_id: UserId for the user. Expected to be unique. Use as table key.
        :param email: email to be used for login.
        :param password: Password to be used for login.
        """
        super().__init__(
            user_id=user_id,
            role=UserRole.Administrator,
            email=email,
            password=password
        )
