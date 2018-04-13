from gui import GUI
from argparse import ArgumentParser
from game import Game, Difficulty, FreeGame
from songs import smoke, lambada, army, popcorn, yesterday, bells, tatu, march


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--scale', default=1.5, type=int)
    scale = parser.parse_args().scale
    songs = [smoke, lambada, army, popcorn, yesterday, bells, tatu, march]
    while True:
        index = 0
        while index < len(songs):
            difficulty = Difficulty(songs[index].tempo + index * 100 // 4, index // 2)
            game = Game(songs[index], difficulty)
            if GUI(game, scale).mainloop():
                index += 1

        GUI(FreeGame(), scale).mainloop()
