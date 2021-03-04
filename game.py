from classes import Game, Maze

def gameloop():
    mygame = Game()
    myMaze = Maze()
    mygame.start()
    while mygame.run:
        myMaze.draw(mygame)
    


if __name__ == "__main__":
    gameloop()