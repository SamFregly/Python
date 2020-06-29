import random

deck = []
n = 52
for i in range(0,n):
    deck.append(i)
print(deck)





def shuffle_human(cards,reshuffle):
    split = random.randint(-1*int(len(cards)/20),int(len(cards)/20)) #creates a bias to imperfectly split deck +- 5% of the deck size
    L = cards[:int(len(cards)/2)+split] # creates left deck
    R = cards[int(len(cards)/2)+split:] # creates right deck
    D =[]                               # empty new deck
    while len(D)< len(cards):           
        bias = random.random()          # creates a bias to "incorrectly" choose 
        if L and bias <=.5:           #     which deck the next card will come from**strong text**
            l = L.pop(0)                # pops the card from the deck and appends it in. 
            #print(l)                    # formatted this way so i can see whats going on 
            D.append(l)     
        if R and bias >.5:           # same thing for right deck
            r = R.pop(0)
            #print(r)
            D.append(r)
    print(D)
    if reshuffle>0:                     # see if there are any reshuffles attempts needed 
        shuffle_human(D,reshuffle-1)  # recursive call to reshuffle the deck. 

shuffle_human(deck,3)
