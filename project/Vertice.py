class Vertice:

    def __init__(self, x, y, reward):
        self.x = x
        self.y = y
        self.reward = reward
        self.is_hashed = False
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_reward( self ):
        return self.reward
    
    def get_hash( self ):
        raise RuntimeError("hash não implementado no vertice")

    def equals( self, vertice ):
        return self.x == vertice.x and self.y == vertice.y and self.reward == vertice.reward
        
    def to_string( self ):
        return "x: " + str( self.x ) + ", y: " + str( self.y ) + ", reward: " + str( self.reward )