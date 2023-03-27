
from otree.api import *
import random
import matplotlib.pyplot as plt
from io import BytesIO
from base64 import b64encode
import urllib

c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'wisdom_of_the_crowd'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    ACTUAL_NUMBER = random.randint(500,1000)
class Subsession(BaseSubsession):
    pass
    
class Group(BaseGroup):
    av_guess = models.FloatField()
    av_devn = models.FloatField()
    avg_devn = models.FloatField()
def average_guess(group: Group):
    players = group.get_players()
    guesses = [p.guess for p in players]
    av_guess = sum(guesses) / C.PLAYERS_PER_GROUP
    group.av_guess = round(av_guess, 3)
    group.av_devn = round(group.av_guess - C.ACTUAL_NUMBER, 3)
    
    group_history = group.in_all_rounds()
    group_history_devn = [g.av_devn for g in group_history]
    group.avg_devn = sum(group_history_devn) / C.NUM_ROUNDS
    # Save the info in highchart format for later use.
    # Get categories for chart (actually currently constant per group):
    hcats = ["Player" + str(id) for id in range(1, C.PLAYERS_PER_GROUP + 1)] + \
            ['Average guess', 'Actual number']
    hdat = guesses + [av_guess] + [C.ACTUAL_NUMBER]  # list of data in appropriate order.
    # Assign the variable to each participant (player across rounds) for later use:
    # TODO: Maybe there is an option to access he group object in js_vars (instead of accessing participant vars)-- I did not see any.
    for p in players:
        p.participant.high_cats = hcats
        p.participant.high_data = [{'name': ix, 'data': [dat]} for ix, dat in zip(hcats, hdat)]
    
class Player(BasePlayer):
    guess = models.FloatField(label='How many balls do you think there are in the box?')
    devn = models.FloatField()
    avg_devn = models.FloatField()
def deviation(player: Player):
    player.devn = round(player.guess - C.ACTUAL_NUMBER, 3)
    
def create_figure(player):
        n = C.ACTUAL_NUMBER
        x = random.sample(range(1, 10000), n)
        y = random.sample(range(1, 10000), n)

        fig, ax = plt.subplots()
        plt.scatter(x, y)
        plt.setp(ax.spines.values(), linewidth=3)
        plt.xticks([])
        plt.yticks([])
        
        fig = plt.gcf()
        buf = BytesIO()        
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)

        string = b64encode(buf.read())

        return urllib.parse.quote(string)
        
def average_devn(player: Player):
    player_history = player.in_all_rounds()
    player_history_devn = [p.devn for p in player_history]
    player.avg_devn = sum(player_history_devn) / C.NUM_ROUNDS
    
class Intro(Page):
    timeout_seconds = 5


class WaitGrouping(WaitPage):
    group_by_arrival_time = True


def group_by_arrival_time_method(subsession, waiting_players):
    if len(waiting_players) >= subsession.session.configs.num_players:
        return waiting_players


class Guess(Page):
    form_model = 'player'
    form_fields = ['guess']
    timeout_seconds = 20
    
    def vars_for_template(player):
       return {'my_img' : create_figure(player)}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        deviation(player)
        
class MyWaitPage(WaitPage):
    after_all_players_arrive = average_guess
        
class Results(Page):       
    form_model = 'player'

    @staticmethod
    def js_vars(player):
        my_dict = {}  # no need to initialize empty dict.
        # my_dict = {player.id_in_group: player.guess}
        # Create dictionary:
        my_dict = {'highchart_cat': player.participant.high_cats,
                   'highchart_dat': player.participant.high_data,
                   }
        
        print("@@@@ my_dict", my_dict)  # print statement for debugging.
        return my_dict
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        average_devn(player)    


class FinalResults(Page):
    form_model = 'player'


page_sequence = [Intro, Guess, MyWaitPage, Results,
                 # FinalResults
                 ]

    
