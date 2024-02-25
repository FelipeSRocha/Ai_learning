class Agente:
    def __init__(self, row, col):
        self.col = int(col)
        self.row = int(row)
        self.alive = True
        self.last_row = -1
        self.last_col = -1

    def move_agent(self, row, col):
        self.last_col = int(self.col)
        self.last_row = int(self.row)        
        self.col = int(col)
        self.row = int(row)
    