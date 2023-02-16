import random

## Note: anything with '##' are considered comments; as such, they are provided
## to aid the reader, and are not part of the solutions. Space in between lines 
## are also done for readibility. 


## Prompt messages

welcome='Would you like to play guess the word? '
seperator='\n..............................\n'
prompt='Please enter a letter or Guess the Word: '
guess=seperator+prompt
correct_already_guessed = 'You have already guessed the letter {0}'
correct_not_guessed = '{0} is in the secret word!'
incorrect_already_guessed = 'You have already incorrectly guessed the letter {0}'
incorrect_not_guessed = '{0} is not in the secret word!'
lives_remaining = 'You only have {0} attempts left.'
guess_remaining = "Would you like to guess the word?"
user_attempt = "Guess the Word:"
incorrect_attempt="Your guess '{0}' is incorrect."
correct_attempt="Your guess '{0}' is correct!"
loss_game = "You ran out of attempts!"
reveal_msg = "Would you like to reveal the word? "

## Chooses a random word in the file

def choose_word():
    f=open('words_.txt', 'r')
    text=f.readlines()
    number=random.randint(1,len(text)-1)
    word_defn = text[number].split('-')
    return word_defn

## Calls the game

def guess_the_word():
    print(seperator)
    
    response = input(welcome).upper()
    
    if response == 'YES':
        word_defn = choose_word()
        secret_word = word_defn[0].upper()
        definition = word_defn[1].upper()
        initial_state='_'*len(secret_word)
        
        if " " in secret_word:
            los = replace_at(secret_word, " ")
            initial_state = list(initial_state)
            for space in los:
                initial_state[space] = ' '
            initial_state="".join(initial_state)
               
        print("Your word is: {}".format(initial_state))
        play (secret_word, definition, initial_state, 0,'', '')
        
    else:
        print('Goodbye')

## returns a list of positions that correspond to the location of the letter
## guess, in the secret word
    
def replace_at (secret_word, guess):
    lop=[ ]
    pos=0
    guess=guess.upper()
    while pos<len(secret_word):
        if secret_word[pos]==guess:
            lop.append(pos)
            pos=pos+1
        else:
            pos=pos+1
    return lop

## replace all instance of the guessed letter in the word_so_far, provided
## that guess is in the secret_word

def replace_occurences(secret_word, current_word, lop):
    replaced=list(current_word)
    for pos in lop:
        replaced[pos]=secret_word[pos]
    return "".join(replaced)


## Main function, where game happens (uses all the helper functions)

def play(secret, definition, current, errors, incorrect, correct):
    
    ## terminates if the game is lost (i.e, number of errors is 10)
    if errors == 10:
        print(seperator)
        print(loss_game)
        reveal = input(reveal_msg).upper()
        if reveal=="YES":
            print(("{0} - {1}").format(secret, definition))
            guess_the_word()
        else:
            guess_the_word()
        
    ## terminates if the game is won (i.e, the current state of the word is the word)
    ## this means, there are no more blanks to fill. 
    
    elif current == secret:
        print(seperator)
        print(("{0} - {1}").format(current, definition))
        print(seperator)
        guess_the_word()
        
    
    ## Neither of the base cases are reached, so the player is still playing.
    
    else:
        
        print('\n')
        
        ## prompts user to guess a letter. 
        guess_input=input(guess).upper()
        
        ## terminates if guess is correct
        if guess_input==secret:
            print("Your guess is correct!")
            print(("{0} - {1}").format(secret, definition))
            guess_the_word()
        
        ## terminates if the guess is incorrect; need to check incase player
        ## guesses a correct component but not the word itself
        elif len(guess_input) > 1:
            print("Your guess is incorrect")
            return play(secret, definition, current, errors+1, incorrect, correct)
            
        
        ## terminates if the guess is in the secret word
        elif guess_input in secret:
            
            ## terminates if the guess has already been guessed 
            if guess_input in correct:
                print(correct_already_guessed.format(guess_input))
                print(current)
                print('Incorrect guesses: {0}'.format(incorrect))
                print('Correct guesses: {0}'.format(correct))
                return play(secret, definition, current, errors, incorrect, correct)
            
            ## terminates if the guess has NOT been guessed
            else:
                ## gathers the positions where replacement occurs
                lop=replace_at(secret, guess_input)
                ## does the replacement of occurences
                update=replace_occurences(secret, current, lop)
                print(correct_not_guessed.format(guess_input))
                print(update)
                print('Incorrect guesses: {0}'.format(incorrect))
                print('Correct guesses: {0}'.format(correct+guess_input))
                ## do not forget to update the parameter 'correct' by adding the 
                ## correct guess, current==update
                return play(secret,definition, update, errors, incorrect, correct+guess_input)
        
        ## terminates if the guess is NOT in the secret word
        else:
            
            ## terminates if guess has already been guessed
            if guess_input in incorrect:
                print(incorrect_already_guessed.format(guess_input))
                print(current)
                print('Incorrect guesses: {0}'.format(incorrect))
                print('Correct guesses: {0}'.format(correct))                
                return play(secret,definition, current, errors, incorrect, correct)
            
            ## terminates if the guess has NOT been guessed
            else:
                print(incorrect_not_guessed.format(guess_input))
                print(current)
                print('Incorrect guesses: {0}'.format(incorrect+guess_input))
                print('Correct guesses: {0}'.format(correct))                
                print(lives_remaining.format(10-(errors)))
                ##do not forget to update the error, and the incorrect guesses
                return play(secret, definition, current, errors+1, incorrect+guess_input, correct)

## Automatically prompts game, when run
guess_the_word()

    
            
