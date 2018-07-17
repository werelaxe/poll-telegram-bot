class Poll:
    def __init__(self, suggestions):
        self.suggestions = set(suggestions)
        self.nickname_to_choice = {}
        self.choice_to_nicknames = dict((s, []) for s in suggestions)

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
        choices = sorted(self.suggestions)
        return 'Опрос: {} или {}?'.format(', '.join(choices[:-1]), choices[-1])