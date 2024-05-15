from util.user_interface import OptionsScreen
from util.user_interface import QuestionnaireScreen
from model.user import User, Administrator, Customer, UserRole
from cart_management import Store


def show_initial_screen() -> str:
    """
    This function shows initial options to user
    :return: The option selected by the user
    """
    initial_screen = OptionsScreen(
        title='Welcome to Monash Merchant',
        options=['Login', 'Exit']
    )
    action = initial_screen.display()
    print(repr(action))
    return action


def show_login_screen() -> Administrator | Customer | None:
    """
    This function shows login questions one by one
    :return: Logged-in user or None
    """
    login_screen = QuestionnaireScreen(
        title='Login',
        question_validators={
            'email': None,
            'password': None}
    )

    response = login_screen.display()

    current_user = User.login(
        email=response['email'],
        password=response['password'],
    )

    if current_user is None:
        print('Login failed')
    else:
        print(f'Logged in as {current_user.role}.')

    return current_user


def show_admin_account_screen(user: Administrator, store: Store | None = None) -> str:
    """
    This functions shows options available to logged-in administrator.
    :param user: Administrator object
    :param store: Store object
    :return: The option selected by the user
    """
    user_screen = OptionsScreen(
        title='Admin account',
        options=['update / delete existing product',
                 'add a new product',
                 'add a new category',
                 'add a new subcategory',
                 'log out']
    )
    action = user_screen.display()
    print(repr(action))
    return action


def show_customer_account_screen(user: Customer, store: Store | None = None) -> str:
    """
    This functions shows options available to logged-in customer.
    :param user: Customer object
    :return: The option selected by the user
    """
    user_screen = OptionsScreen(
        title=f'{user.first_name} {user.last_name} ({user.email})\n'
              'Welcome to Monash Merchant supermarket',
        options=['go to Account Management',
                 'go to Products',
                 'go to shopping cart',
                 'log out']
    )
    action = user_screen.display()
    print(repr(action))
    if action == 'go to Products' or action == 'go to shopping cart':
        if not store:
            store = Store()
        if action == 'go to Products':
            store.display_products()
        elif action == 'go to shopping cart':
            store.run()
    return action


def main() -> None:
    """
    This is the entry point for the app
    :return: None
    """
    store = None
    while True:
        user_action = show_initial_screen()

        if user_action == 'Exit':
            break

        user = show_login_screen()
        if user is None:
            print('Invalid email or password')
            continue

        if user.role == UserRole.Administrator:
            while True:
                user_action = show_admin_account_screen(user, store)
                if user_action == 'log out':
                    break
                if user_action == 'update / delete existing product':
                    pass  # TODO: Add action
                elif user_action == 'add a new product':
                    pass  # TODO: Add action
                elif user_action == 'add a new category':
                    pass  # TODO: Add action
                elif user_action == 'add a new subcategory':
                    pass  # TODO: Add action
        elif user.role == UserRole.Customer:
            store = None
            while True:
                user_action = show_customer_account_screen(user, store)
                if user_action == 'log out':
                    break
                if user_action in ['go to Account Management', 'go to Products', 'go to shopping cart']:
                    continue


if __name__ == '__main__':
    # print('sehej is here')
    # demo push
    # store = Store()
    main()
