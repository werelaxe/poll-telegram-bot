class Poll:
    def __init__(self, suggestions, title_prefix='Опрос: '):
        self.suggestions = suggestions
        self.nickname_to_choice = {}
        self.choice_to_nicknames = dict((s, []) for s in suggestions)
        self.title_prefix = title_prefix

    def vote(self, nickname, choice):
        if choice not in self.suggestions:
            raise ValueError("Bad suggestion: {}".format(choice))
        if self.is_nickname_did_choice(nickname):
            if self.nickname_to_choice[nickname] == choice:
                self.remove_choice(nickname)
            else:
                self.remove_choice(nickname)
                self.add_choice(nickname, choice)
        else:
            self.add_choice(nickname, choice)

    def remove_choice(self, nickname):
        self.choice_to_nicknames[self.nickname_to_choice[nickname]].remove(nickname)
        self.nickname_to_choice.pop(nickname)

    def add_choice(self, nickname, choice):
        self.nickname_to_choice[nickname] = choice
        self.choice_to_nicknames[choice].append(nickname)

    def is_nickname_did_choice(self, nickname):
        return nickname in self.nickname_to_choice

    def get_results(self):
        lines = [
            choice + ': ' +
            ', '.join(['@' + nick for nick in sorted(nicknames)]) for choice, nicknames in self.choice_to_nicknames.items()
        ]
        stat = dict(
            (choice, len(nicknames))
            for choice, nicknames in self.choice_to_nicknames.items()
        )
        return '\n'.join(lines), stat

    def get_title(self):
        choices = self.suggestions
        return '{}{} или {}?'.format(self.title_prefix, ', '.join(choices[:-1]), choices[-1])


def create_new_dinner_time_poll():
    return Poll(['13:00', '13:30', '14:00', '14:30', '15:00'], "Когда на обед? В ")


def create_new_dinner_place_poll():
    return Poll(['Тревелерс', 'Рататуй', 'Столовая', 'Гастроли', 'Гады, крабы и вино'], 'Куда на обед? В ')


def create_new_breakfast_time_poll():
    return Poll(['9:00', '9:30', '10:00', '10:30'], 'Когда на завтрак? В ')
