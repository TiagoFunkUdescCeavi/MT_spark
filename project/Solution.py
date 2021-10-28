from Utils import calculate_distance

class Solution:    
    def __init__( self, number_paths, time_per_path ) -> None:
        self.number_paths = number_paths
        self.paths = []
        self.path_rewards = []
        self.path_times = []
        for i in range( number_paths ):
            self.paths.append( [] )
            self.path_rewards.append( 0.0 )
            self.path_times.append( 0.0 )
        self.time_per_path = time_per_path
        self.total_rewards = 0.0
        self.total_time = 0.0
        self.used_vertices = []
    
    def add_initial_and_final_vertices( self, path, initial_vertice, final_vertice ):
        if self.check_if_path_is_valid( path ):
            raise RuntimeError("Erro")
        new_time = calculate_distance( initial_vertice, final_vertice )
        if self.time_per_path < new_time:
            raise RuntimeError("Erro")
        self.paths[ path ].append( initial_vertice )
        self.paths[ path ].append( final_vertice )
        self.path_times[ path ] = new_time
        self.total_time += new_time

    def update_time_per_path( self, time_per_path ):
        self.time_per_path = time_per_path

    def update_reward_in_add( self, path, vertice ):
        self.path_rewards[ path ] += vertice.get_reward()
        self.total_rewards += vertice.get_reward()
    
    def update_reward_in_rewrite( self, path, position, v ):
        vertice_to_remove          = self.paths[ path ][ position ]
        self.path_rewards[ path ] -= vertice_to_remove.get_reward()
        self.total_rewards        -= vertice_to_remove.get_reward()
        self.path_rewards[ path ] += v.get_reward()
        self.total_rewards        += v.get_reward()

    def update_reward_in_remove( self, path, position ):
        vertice_to_remove = self.paths[ path ][ position ]
        self.path_rewards[ path ] -= vertice_to_remove.get_reward()
        self.total_rewards -= vertice_to_remove.get_reward()
    
    def update_time( self, path, new_time ):
        if self.check_if_path_is_valid( path ):
            return
        self.total_time += new_time - self.path_times[ path ]
        self.path_times[ path ] = new_time

    def add_in_path( self, path, position, vertice ):
        self.paths[ path ].insert( position, vertice )
        self.used_vertices.append( vertice )
    
    def remove_in_path( self, path, position ):
        v = self.paths[ path ][ position ]
        self.used_vertices.remove( v )
        self.paths[ path ].remove( v )

    def calculate_time_in_add( self, path, position, v ):
        previous = self.paths[ path ][ position-1 ]
        next     = self.paths[ path ][ position ]
        old_distance             = calculate_distance( previous, next )
        new_distance_to_previous = calculate_distance( previous, v )
        new_distance_to_next     = calculate_distance( next, v )
        return self.path_times[ path ] - old_distance + new_distance_to_previous + new_distance_to_next

    def calculate_time_in_rewrite( self, path, position, v ):
        previous = self.paths[ path ][ position-1 ]
        middle   = self.paths[ path ][ position ]
        next     = self.paths[ path ][ position+1 ]
        old_dist_to_previous = calculate_distance( previous, middle )
        old_dist_to_next     = calculate_distance( middle, next )
        new_dist_to_previous = calculate_distance( previous, v )
        new_dist_to_next     = calculate_distance( v, next )
        return self.path_times[ path ] - old_dist_to_previous - old_dist_to_next + new_dist_to_previous + new_dist_to_next
    
    def calculate_time_in_remove( self, path, position ):
        previous = self.paths[ path ][ position-1 ]
        middle   = self.paths[ path ][ position ]
        next     = self.paths[ path ][ position+1 ]
        old_distance_to_previous = calculate_distance( previous, middle )
        old_distance_to_next     = calculate_distance( middle, next )
        new_distance             = calculate_distance( previous, next )
        return self.path_times[ path ] - old_distance_to_previous - old_distance_to_next + new_distance
    
    def recalculate_time( self, path ):
        sum = 0.0
        for i in range( len( self.paths[ path ] ) ):
            sum += calculate_distance( self.paths[ path ][ i ], self.paths[ path ][ i+1 ] )
        return sum
    
    def check_if_vertice_is_used( self, vertice ):
        for v in self.used_vertices:
            if vertice.equals( v ):
                return True
        return False
    
    def check_if_path_is_valid( self, path ):
        return path < 0 and path >= len( self.paths )
    
    def check_if_path_position_is_valid( self, path, position ):
        return self.check_if_path_is_valid( path ) and ( position < 1 and position >= len( self.paths[ path ] ) )
    
    def check_if_position_is_initial_or_final( self, path, position ):
        size = len( self.paths[ path ] ) -1
        return position == 0 and position == size
    
    def add( self, path, v ):
        if( self.check_if_path_is_valid( path ) ):
            return False
        position = len( self.paths[ path ] ) - 1
        return self.add_in_position( path, position, v )
    
    def add_in_position( self, path, position, v ):
        if self.check_if_path_position_is_valid( path, position ):
            return False
        if self.check_if_vertice_is_used( v ) :
            return False
        if v == None :
            return False
    
        new_time = self.calculate_time_in_add( path, position, v )

        if( self.time_per_path > new_time ):
            self.update_reward_in_add( path, v )
            self.add_in_path( path, position, v )
            self.update_time( path, new_time )
            return True
    
        return False

    def rewrite( self, path, position, v ):
        if self.check_if_path_position_is_valid( path, position ) :
            return False
        if self.check_if_vertice_is_used( v ) :
            return False

        new_time = self.calculate_time_in_rewrite( path, position, v )

        if self.time_per_path > new_time :
            self.update_reward_in_rewrite( path, position, v )
            self.remove_in_path( path, position )
            self.add_in_path( path, position, v )
            self.update_time( path, new_time )
            return True
    
        return False

    def swap( self, path, pos1, pos2 ):
        if self.check_if_path_position_is_valid( path, pos1 ) :
            return False
        if self.check_if_path_position_is_valid( path, pos2 ) :
            return False

        v = self.paths[ path ][ pos1 ]
        self.paths[ path ][ pos1 ] = self.paths[ path ][ pos2 ]
        self.paths[ path ][ pos2 ] = v

        new_time = self.recalculate_time( path )

        if self.time_per_path > new_time :
            self.update_time( path, new_time )
            return True
        else:
            v = self.paths[ path ][ pos1 ]
            self.paths[ path ][ pos1 ] = self.paths[ path ][ pos2 ]
            self.paths[ path ][ pos2 ] = v
            return False
    
    def swap( self, path1, pos1, path2, pos2 ):
        if( self.check_if_path_position_is_valid( path1, pos1 ) ):
            return False
        if( self.check_if_path_position_is_valid( path2, pos2 ) ):
            return False
        if( self.check_if_position_is_initial_or_final( path1, pos1 ) ):
            return False
        if( self.check_if_position_is_initial_or_final( path2, pos2 ) ):
            return False

        reward_1 = self.paths[ path1 ][ pos1 ].get_reward()
        reward_2 = self.paths[ path2 ][ pos2 ].get_reward()

        v = self.paths[ path1 ][ pos1 ]
        self.paths[ path1 ][ pos1 ] = self.paths[ path2 ][ pos2 ]
        self.paths[ path2 ][ pos2 ] = v

        new_time_path_1 = self.recalculate_time( path1 )
        new_time_path_2 = self.recalculate_time( path2 )

        if( (self.time_per_path > new_time_path_1 and self.time_per_path > new_time_path_2) ):
            self.update_time( path1, new_time_path_1 )
            self.update_time( path2, new_time_path_2 )
            self.path_rewards[ path1 ] += reward_2 - reward_1
            self.path_rewards[ path2 ] += reward_1 - reward_2
            return True
        else:
            v = self.paths[ path1 ][ pos1 ]
            self.paths[ path1 ][ pos1 ] = self.paths[ path2 ][ pos2 ]
            self.paths[ path2 ][ pos2 ] = v
            return False

    def remove( self, path, position ):
        if( self.check_if_path_position_is_valid( path, position ) ):
            return False
        self.update_reward_in_remove( path, position )
        new_time = self.calculate_time_in_remove( path, position )
        self.update_time( path, new_time )
        self.remove_in_path( path, position )
        return True
    
    def move( self, path1, position1, path2, position2 ):
        if( self.check_if_path_position_is_valid( path1, position1 ) ):
            return False
        if( self.check_if_path_position_is_valid( path2, position2 ) ):
            return False

        v = self.paths[ path1 ][ position1 ]

        new_time_path_1 = self.calculate_time_in_remove( path1, position1 )
        new_time_path_2 = self.calculate_time_in_add( path2, position2, v )

        if( self.time_per_path > new_time_path_2 ):
            self.update_time( path1, new_time_path_1 )
            self.update_time( path2, new_time_path_2 )
            self.update_reward_in_remove( path1, position1 )
            self.remove_in_path( path1, position1 )
            self.update_reward_in_add( path2, v )
            self.add_in_path( path2, position2, v )
            return True
        
        return False
    
    def is_empty( self, path ):
        if( self.check_if_path_is_valid( path ) ):
            return True
        return len( self.paths[ path ] ) != 2
    
    def get_last_path_vertice_in_path( self, path ):
        if( self.check_if_path_is_valid( path ) ):
            return None
        last_position = len( self.paths[ path ] ) - 1 - 1
        return self.paths[ path ][ last_position ]
    
    def get_vertice_in_path( self, path, position ):
        if( self.check_if_path_position_is_valid( path, position ) ):
            return None
        return self.paths[ path ][ position ]
    
    def get_rewards( self, path ):
        if( not self.check_if_path_is_valid( path ) ):
            return self.path_rewards[ path ]
    
    def get_total_rewards( self ):
        return self.total_rewards
    
    def get_total_time( self ):
        return self.total_time
    
    def get_distance( self, path, position ):
        if( self.check_if_path_position_is_valid( path, position ) ):
            return -1.0
        if( len( self.paths[ path ] ) == 2 ):
            return -1.0
        distance = calculate_distance( self.paths[ path ][ position-1 ], self.paths[ path ][ position ] )
        distance += calculate_distance( self.paths[ path ][ position ], self.paths[ path ][ position+1 ] )
        return distance
    
    def get_time_path( self, path ):
        if( self.check_if_path_is_valid( path ) ):
            return -1.0
        return self.path_times[ path ]

    def get_time_per_path( self ):
        return self.time_per_path
    
    def get_number_paths( self ):
        return len( self.paths )

    def get_length_of_path( self, path ):
        if self.check_if_path_is_valid( path ):
            return -1
        return len( self.paths[ path ] )
    
    def get_total_length_of_path( self ):
        sum = 0
        for i in range( len( self.paths ) ):
            sum += len( self.paths[ i ] ) - 2
        return sum
    
    def to_string( self ):
        s = "number paths: " + str( len( self.paths ) ) + "\n"
        s += "paths:\n"
        position = 0
        for path in self.paths:
            s += "size: " + str( len( path ) ) + "\n"
            for vertice in path:
                s += vertice.to_string() + "\n"
            s += "reward: " + str( self.path_rewards[ position ] ) + "\n"
            s += "time: " + str( self.path_times[ position ] ) + "\n"
            s += ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
            position += 1
        
        s += "time per path: " + str( self.time_per_path ) + "\n"
        s += "total reward: " + str( self.total_rewards ) + "\n"
        s += "total time: " + str( self.total_time ) + "\n"
        #s += "hash: " + str( self.get_hash() ) + "\n"
        
        return s