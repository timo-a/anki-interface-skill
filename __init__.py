from mycroft import MycroftSkill, intent_file_handler
from subprocess import Popen, PIPE
import pyautogui
import enum
import time


# Using enum class create enumerations
class InternalState(enum.Enum):
    Menu              = 1
    Deck_Review       = 2
    Answer_Evaluation = 3


class AnkiInterface(MycroftSkill):

    def __init__(self):
        MycroftSkill.__init__(self)
        self.internal_state = None
        self.anki_process = None

    def initialize(self):
        self.register_entity_file('decknr.entity')

    @intent_file_handler('open.anki.intent')
    def handle_open_anki_intent(self, message):
        self.speak_dialog('open.anki')
        self.anki_process = Popen(['anki'], stdin=PIPE, shell=True)
        self.internal_state = InternalState.Menu

        number_of_decks = self.settings.get('number of decks')
        if number_of_decks is None or number_of_decks < 0:
            self.update_number_of_decks()

    def update_number_of_decks(self):
        user_input = self.get_response('ask.number.of.decks')
        if user_input in dni_dic:
            new_deck_nr = dniparser(user_input)
            self.settings['number of decks'] = new_deck_nr
            self.speak(f"I've updated the number of decks to {new_deck_nr}")
        else:
            self.speak(f"I cannot handle the number you provided: {user_input}, sorry")

    @intent_file_handler('update.number.of.decks')
    def handle_update_number_of_decks(self, message):
        self.update_number_of_decks()

    @intent_file_handler('open.deck.intent')
    def handle_open_deck(self, message):
        # self.anki_process.communicate(input='\n')
        dn = message.data.get('decknr')
        print(f"per print: {dn}")
        self.log.info(f"dn: {dn}")
        if dn is not None:
            # self.speak_dialog('open.deck', {'decknumber': dn})

            dni = dniparser(dn)
            # if user input is too high we just take the last deck

            nr_of_decks = self.settings.get('number of decks')
            if dni > nr_of_decks:
                dni = nr_of_decks
                self.log.info(f"user has asked for deck {dn} but according to settings there are only {nr_of_decks} so we take that.")

            self.speak_dialog('open.deck', {'decknumber': dni})
            pyautogui.hotkey('alt', 't')
            pyautogui.hotkey('enter')

            time.sleep(1)

            #ensure uppermost deck is selected
            #default selected is the deck called 'default' but there may be decks above
            pyautogui.hotkey(' ')
            pyautogui.hotkey('backspace')

            time.sleep(1)
            
            for _ in range(dni - 1):
                pyautogui.hotkey('down')
            pyautogui.hotkey('enter')
            pyautogui.hotkey('space')
            self.internal_state = InternalState.Deck_Review
        else:
            self.speak_dialog('open.deck.none')

    @intent_file_handler('show.answer.intent')
    def handle_show_answer(self, message):
        self.log.debug('recpgnized show d  intent')
        self.log.info ('recpgnized show i intent')

        pyautogui.hotkey('space')
        self.internal_state = InternalState.Answer_Evaluation
        self.speak(utterance="", expect_response=True) # so user doesn't have to say 'Hi mycroft' all the time.


    @intent_file_handler('verdict.again.intent')
    def handle_verdict_again(self, message):
        self.log.info ('recognized verdict again intent')
        pyautogui.hotkey('shift', 'tab')
        pyautogui.hotkey('shift', 'tab')
        pyautogui.hotkey('space')
        self.internal_state = InternalState.Deck_Review
        self.speak(utterance="", expect_response=True)

    @intent_file_handler('verdict.hard.intent')
    def handle_verdict_hard(self, message):
        self.log.info('recognized verdict hard intent')
        pyautogui.hotkey('shift', 'tab')
        pyautogui.hotkey('space')
        self.internal_state = InternalState.Deck_Review
        self.speak(utterance="", expect_response=True)

    @intent_file_handler('verdict.good.intent')
    def handle_verdict_good(self, message):
        self.log.info('recognized verdict good intent')
        pyautogui.hotkey('space')
        self.internal_state = InternalState.Deck_Review
        self.speak(utterance="", expect_response=True)

    @intent_file_handler('verdict.easy.intent')
    def handle_verdict_easy(self, message):
        self.log.info('recognized easy intent')
        pyautogui.hotkey('tab')
        pyautogui.hotkey('space')
        self.internal_state = InternalState.Deck_Review
        self.speak(utterance="", expect_response=True)

    @intent_file_handler('verdict.againof3.intent')
    def handle_verdict_again(self, message):
        """
             regular options: [again] [hard] [good] [easy]
             on new cards:    [again]        [good] [easy]
             so we need a spacial again intent for new cards (which occur rarely)
        """
        self.log.info('recognized again intent on new card')
        pyautogui.hotkey('shift', 'tab')
        pyautogui.hotkey('space')
        self.internal_state = InternalState.Deck_Review
        self.speak(utterance="", expect_response=True)




    @intent_file_handler('undo.verdict.intent')
    def handle_verdict_undo(self, message):
        self.log.debug('recognized easy intent')
        pyautogui.hotkey('ctrl', 'alt', 'z')
        self.internal_state = InternalState.Deck_Review
        self.speak(utterance="", expect_response=True)

    @intent_file_handler('back.to.menu.intent')
    def handle_back_to_menu(self, message):
        pyautogui.hotkey('d')
        self.internal_state = InternalState.Menu

    @intent_file_handler('quit.intent')
    def handle_quit(self, message):
        pyautogui.hotkey('ctrl', 'q')
        try:
            self.anki_process.kill()  # just to make sure it's finished
        except:
            pass
        self.internal_state = None





dni_dic_base = {1: "1 one won",
                2: "2 two to too",
                3: "3 three",
                4: "4 four for",
                5: "5 five",
                6: "6 six",
                7: "7 seven",
                8: "8 eight",
                9: "9 nine",
               10: "10 ten",
               11: "11 eleven",
               12: "12 twelve",
               13: "13 thirteen",
               14: "14 fourteen",
               15: "15 fifteen",
               16: "16 sixteen",
               17: "17 seventeen",
               18: "18 eighteen",
               19: "19 nineteen",
               20: "20 twenty"}
# I assume no one has more than 20 decks

dni_dic = {variant:a for a,b in dni_dic_base.items() for variant in b.split()}

def dniparser(token):
    if token in dni_dic:
        return dni_dic[token]
    else:
        raise Exception("Decknumber accepted by padatious but"+
                        "can't be parsed in __init__")


def create_skill():
    return AnkiInterface()
