
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'my_public_goods'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 3
    ENDOWMENT = 1000
    MULTIPLIER = 2
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    for player in players:
        player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
class Player(BasePlayer):
    contribution = models.CurrencyField(label='How much do you want to contribute?', max=1000, min=0)
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']
class Wait_for_results(WaitPage):
    after_all_players_arrive = set_payoffs
    body_text = 'Wait for others to contribute'
class MyPage(Page):
    form_model = 'player'
page_sequence = [Contribute, Wait_for_results, MyPage]