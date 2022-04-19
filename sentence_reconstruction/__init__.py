
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'sentence_reconstruction'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    SENTENCE = 'In the hours of the waking night, unholy creatures roam, and settle in the abyss of your thoughts'
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    reconstructed_sentence = models.StringField()
def aggregate(group: Group):
    players = group.get_players()
    group.reconstructed_sentence = str([p.remembered_sentence for p in players])
    
    
class Player(BasePlayer):
    Name = models.StringField()
    remembered_sentence = models.StringField(blank=True)
    final_sentence = models.StringField()
class Sentence(Page):
    form_model = 'player'
    timeout_seconds = 10
class Individual_memory(Page):
    form_model = 'player'
    form_fields = ['Name', 'remembered_sentence']
class MyWaitPage(WaitPage):
    after_all_players_arrive = aggregate
class Group_memory(Page):
    form_model = 'player'
    form_fields = ['final_sentence']
class Results(Page):
    form_model = 'player'
page_sequence = [Sentence, Individual_memory, MyWaitPage, Group_memory, Results]