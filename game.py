class Game:
    def __init__(self, id):
        self.ready = False
        self.id = id
        self.moves = [None, None]
        # self.wins = [0, 0]
        self.last = -1

    def get_player_move(self, p):
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.last = 0
        else:
            self.last = 1

    def connected(self):
        return self.ready

    def get_last(self):
        return self.last

    def get_end(self):
        return True if self.moves[0] == '0,5' or self.moves[1] == '0,5' else False

    def winner(self):

        p1 = self.moves[0]
        p2 = self.moves[1]
        winner = -1
        if p1 == '0,5':
            winner = 1
        if p2 == '0,5':
            winner = 0

        return winner

