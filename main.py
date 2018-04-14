from gui import GUI
from argparse import ArgumentParser
from game import Game, Difficulty, FreeGame
from songs import smoke, lambada, army, popcorn, yesterday, bells, tatu, march


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--scale', default=1.5, type=float)
    scale = parser.parse_args().scale
    songs = [smoke, lambada, army, tatu, popcorn, bells, yesterday, march]
    while True:
        index = 0
        while index < len(songs):
            song = songs[index]
            difficulty = Difficulty(song.tempo + index * 100 // 2 + len(song.keys) * 10, index // 2)
            game = Game(song, difficulty)
            if GUI(game, scale).mainloop():
                index += 1

        GUI(FreeGame(), scale).mainloop()
