
from otree.api import *
import spacy

c = cu
nlp = spacy.load('en_core_web_sm')

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'sentence_reconstruction'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1

    SENTENCE_TO = 10  # timeout time for sentence.

    SENTENCE = 'In the hours of the waking night, locusts march in circles, and never settle in the abyss of your thoughts'
    ref_doc = nlp(u'In the hours of the waking night, locusts march in circles, and never settle in the abyss of your thoughts')
    # Was:
    # SENTENCE = 'In the hours of the waking night, unholy creatures roam, and settle in the abyss of your thoughts'
    # ref_doc = nlp(u'In the hours of the waking night, unholy creatures roam, and settle in the abyss of your thoughts')



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    reconstructed_sentence = models.StringField()


def aggregate(group: Group):
    players = group.get_players()
    group.reconstructed_sentence = str([p.remembered_sentence for p in players])
    
    
class Player(BasePlayer):
    #Name = models.StringField()
    remembered_sentence = models.StringField(blank=True)
    doc1 = nlp(str(remembered_sentence))
    final_sentence = models.StringField()
    doc2 = nlp(str(final_sentence))
    initial_similarity = models.FloatField(initial=1)
    final_similarity = models.FloatField(initial=0.5)
    

def compare(player: Player):
    player.doc1 = nlp(str(player.remembered_sentence))
    player.doc2 = nlp(str(player.final_sentence))
    player.initial_similarity = round(player.doc1.similarity(C.ref_doc),3)
    player.final_similarity = round(player.doc2.similarity(C.ref_doc),3)
    player.participant.sim_cats = ['Initial', 'Final']
    player.participant.sim_data = [{'name':'Initial', 'data':[player.initial_similarity]}, {'name':'Final', 'data':[player.final_similarity]}]


class SentenceInstr(Page):
    pass


class Sentence(Page):
    form_model = 'player'
    timeout_seconds = C.SENTENCE_TO

class Individual_memory(Page):
    form_model = 'player'
    form_fields = ['remembered_sentence']

class MyWaitPage(WaitPage):
    after_all_players_arrive = aggregate


class Group_memory(Page):
    form_model = 'player'
    form_fields = ['final_sentence']
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        compare(player)

    @staticmethod
    def vars_for_template(player: Player):
        return dict(sentences=eval(player.group.reconstructed_sentence))


class Results(Page):
    form_model = 'player'
    @staticmethod
    def js_vars(player):
        similarity_dict = {'similarity_cat': player.participant.sim_cats, 
                           'similarity_dat': player.participant.sim_data,
                           }
        print(similarity_dict)
        return similarity_dict


page_sequence = [SentenceInstr, Sentence, Individual_memory, MyWaitPage, Group_memory, Results]