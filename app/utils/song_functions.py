from random import randint

def calculate_potential_scores(position: int)-> tuple:
    """
    Calculate the potential scores for a song based on its position in the final ranking
    returns a tuple: (jury_potential_score, televote_potential_score)
    """
    if position in range(1,4):
        return (randint(9, 10), randint(9, 10))
    
    elif position in range (4, 6):
        return (randint(8, 9), randint(8, 9))
    
    elif position in range (6, 11):
        return (randint(7, 9), randint(7, 9))
    
    elif position in range (11, 16):
        return (randint(6, 8), randint(6, 8))
    
    elif position in range (16, 21):
        return (randint(5, 7), randint(5, 7))
    
    elif position in range (21, 28):
        return (randint(2, 5), randint(2, 5))
    
    else:
        return (randint(1, 4), randint(1, 4))