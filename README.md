# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/brain.svg" card_color="#0000FF" width="50" height="50" style="vertical-align:bottom"/> Anki Interface
Control the flashcard program anki with your voice.

## About
Control the flashcard program anki with your voice. mycroft navigates anki by sending key presses.

## Examples
### Start Up
* "Open anki"
* "Start vocabulary review"
### Open a deck
* "Open deck two"
* "Open deck number two"
### navigate through a deck
* "show"
* "show answer"
* "easy"
* "good"
* "hard"
* "again"
* "again on new" 
if the card is new there are only 3 answers and "again" is closer to the default, so we need a separate intent with a different cue.
* undo
### exiting
* "go back to main menu"
* "quit"

## Credits
timo-a

## Short Demo
https://youtu.be/Hl4csl_IDmc 

## Installation

    msm install https://github.com/timo-a/anki-interface-skill.git

should work. If not make sure `pyautogui` is installed

## Category
**Daily**
Productivity

## Tags
#Spaced repetition
#Vocab
#Learning

