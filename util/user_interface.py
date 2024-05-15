from typing import Dict


class Screen(object):
    """This class represents a screen presented to the user"""

    def __init__(self, title: str) -> None:
        """
        The __init__ method for Screen.
        :param title: The title for the screen
        """
        self.title = title

    def display(self):
        """
        Placeholder method
        :return: Depends on the subclass
        """
        raise NotImplementedError("Subclasses must implement display method")


class OptionsScreen(Screen):
    """This class represents a screen where user can choose from a list of options"""

    def __init__(self, title: str, options: list) -> None:
        """
        The __init__ method for OptionsScreen
        :param title: The title for the screen
        :param options: A list of available options as str
        """
        super().__init__(title)
        self.options = options

    def display(self) -> str | None:
        """
        The display method for OptionsScreen
        :return: The selected option as a str
        """
        while True:
            print('\n'
                  '----------------\n'
                  f'{self.title}\n'
                  '----------------\n')
            for idx, option in enumerate(self.options, start=1):
                print(f"Enter {idx} to {option}")
            choice = self._get_user_input()
            if choice is None:
                return None
            return self.options[choice]

    def _get_user_input(self) -> int | None:
        """
        Get a valid input from the user
        :return: index of the selected option
        """
        while True:
            try:
                choice = int(input("\nEnter the number of your choice: "))
                if 1 <= choice <= len(self.options):
                    return choice - 1
                else:
                    print("Invalid choice. Please enter a number between 1 and", len(self.options))
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                return None


class QuestionnaireScreen(Screen):
    """This class represents a screen where user can can answer a list of questions"""

    def __init__(self, title: str,
                 question_validators: Dict[str, str | None],
                 question_hints: Dict[str, str] | None = None) -> None:
        """
        he __init__ method for QuestionnaireScreen
        :param title: The title for the screen
        :param question_validators: A dict giving questions to ask and optionally validators
        :param question_hints: A dict giving questions to ask and validation hints
        """
        super().__init__(title)
        self.questions = list(question_validators.keys())
        self.validators = list(question_validators.values())
        if question_hints is None:
            question_hints = {}
        self.hints = [question_hints[q] if q in question_hints else None for q in self.questions]

    def display(self) -> Dict[str, str] | None:
        """
        The display method for QuestionnaireScreen
        :return: The provided answers to each question as a dict
        """
        response = {}
        for idx, question in enumerate(self.questions):
            validator = self.validators[idx]
            if validator is None:
                def accept_anything(_):
                    return True

                validator = accept_anything
            hint = self.hints[idx]

            try:
                answer = None
                while answer is None:
                    answer = input(f'\nPlease enter {question}: ')
                    if not validator(answer):
                        if hint is not None:
                            print(hint)
                        answer = None
                response[question] = answer
            except KeyboardInterrupt:
                return None
        else:
            return response
