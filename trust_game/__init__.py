
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'trust_game'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    MULTIPLIER = 3
    ENDOWMENT = cu(10)
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    sent_amount = models.CurrencyField(label='How much are you willing to send to your partner?', max=10, min=0)
    sent_back_amount = models.CurrencyField(label='How much will you send back to player 1?')
def sent_back_amount_choices(group: Group):
    return currency_range(
            0,
            group.sent_amount * C.MULTIPLIER,
            1
        )
def set_payoffs(group: Group):
    #p1 = group.get_player_by_id(1)
    #p2 = group.get_player_by_id(2)
    group.get_player_by_id(1).payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount
    group.get_player_by_id(2).payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount
class Player(BasePlayer):
    pass
class Send_page(Page):
    form_model = 'group'
    form_fields = ['sent_amount']
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 1
class Player2wait(WaitPage):
    body_text = 'Please wait for your partner to send you money'
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 2
class Send_back_money(Page):
    form_model = 'group'
    form_fields = ['sent_back_amount']
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 2
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        group
        return dict(tripled_amount=group.sent_amount * C.MULTIPLIER)
class Player1wait(WaitPage):
    after_all_players_arrive = set_payoffs
    body_text = 'Please wait for your partner to decide'
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 1
class Results(Page):
    form_model = 'player'
page_sequence = [Send_page, Player2wait, Send_back_money, Player1wait, Results]