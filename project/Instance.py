class Instance:
    def __init__(self) -> None:
        self.number_vertices = 0
        self.number_null_vertices = 0
        self.number_path_vertices = 0
        self.number_paths = 0
        self.time_per_path = 0.0
        self.initial_vertice = None
        self.final_vertice = None
        self.vertices_on_path = []
    
    def set_number_vertices( self, number_vertices ):
        self.number_vertices = number_vertices
    
    def set_number_paths( self, number_paths ):
        self.number_paths = number_paths
    
    def set_time_per_path( self, time_per_path ):
        self.time_per_path = time_per_path
    
    def add_point( self, vertice ):
        if vertice.get_reward() == 0:
            self.number_null_vertices += 1

            if self.initial_vertice == None:
                self.initial_vertice = vertice
            elif self.initial_vertice != None:
                self.final_vertice = vertice
        else:
            self.number_path_vertices += 1
            self.vertices_on_path.append( vertice )
    
    def get_number_vertices( self ):
        return self.number_vertices
    
    def get_number_null_vertices( self ):
        return self.number_null_vertices
    
    def get_number_path_vertices( self ):
        return self.number_path_vertices
    
    def get_number_paths( self ):
        return self.number_paths
    
    def get_time_per_path( self ):
        return self.time_per_path
    
    def get_vertice_on_path( self, position ):
        return self.vertices_on_path[ position ]
    
    def get_vertices_on_path( self ):
        vp = []
        for v in self.vertices_on_path:
            vp.append( v )
        return vp
    
    def get_initial_vertice( self ):
        return self.initial_vertice
    
    def get_final_vertice( self ):
        return self.final_vertice
    
    def to_string( self ):
        s = "Vertices: " + str( self.number_vertices ) + "\n"
        s += "Paths: " + str( self.number_paths ) + "\n"
        s += "Time: " + str( self.time_per_path ) + "\n"
        s += "Points:\n"
        for i in self.vertices_on_path:
            s += i.to_string() + "\n"
        return s