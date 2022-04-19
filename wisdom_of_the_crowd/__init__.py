
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'wisdom_of_the_crowd'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    ACTUAL_NUMBER = 200
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    av_guess = models.FloatField()
def average_guess(group: Group):
    players = group.get_players()
    guesses = [p.guess for p in players]
    group.av_guess = sum(guesses) / C.PLAYERS_PER_GROUP
    
class Player(BasePlayer):
    guess = models.FloatField(label='How many balls do you think there are in the box?')
    devn = models.FloatField()
def deviation(player: Player):
    player.devn = player.guess - C.ACTUAL_NUMBER
class Guess(Page):
    form_model = 'player'
    form_fields = ['guess']
    timeout_seconds = 100
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        deviation(player)
class MyWaitPage(WaitPage):
    after_all_players_arrive = average_guess
class Results(Page):
    form_model = 'player'
page_sequence = [Guess, MyWaitPage, Results]