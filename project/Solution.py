from Utils import calculate_distance
from Vertice import Vertice

class Solution:    
    def __init__( self, number_paths: int, time_per_path: float ):
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

    def update_time_per_path( self, time_per_path: float ):
        self.time_per_path = time_per_path

    def __update_reward_in_add( self, path: int, vertice: Vertice ):
        self.path_rewards[ path ] += vertice.get_reward()
        self.total_rewards += vertice.get_reward()
    
    def __update_reward_in_rewrite( self, path: int, position: int, v: Vertice ):
        vertice_to_remove          = self.paths[ path ][ position ]
        self.path_rewards[ path ] -= vertice_to_remove.get_reward()
        self.total_rewards        -= vertice_to_remove.get_reward()
        self.path_rewards[ path ] += v.get_reward()
        self.total_rewards        += v.get_reward()

    def __update_reward_in_remove( self, path: int, position: int ):
        vertice_to_remove = self.paths[ path ][ position ]
        self.path_rewards[ path ] -= vertice_to_remove.get_reward()
        self.total_rewards -= vertice_to_remove.get_reward()
    
    def __update_time( self, path: int, new_time: float ):
        if self.__check_if_path_is_valid( path ):
            return
        self.total_time += new_time - self.path_times[ path ]
        self.path_times[ path ] = new_time

    def __add_in_path( self, path: int, position: int, vertice: Vertice ):
        self.paths[ path ].insert( position, vertice )
    
    def __remove_in_path( self, path: int, position: int ):
        v = self.paths[ path ][ position ]
        self.paths[ path ].remove( v )

    def __calculate_time_in_add( self, path: int, position: int, v: Vertice ):
        previous = self.paths[ path ][ position-1 ]
        next     = self.paths[ path ][ position ]
        old_distance             = calculate_distance( previous, next )
        new_distance_to_previous = calculate_distance( previous, v )
        new_distance_to_next     = calculate_distance( next, v )
        return self.path_times[ path ] - old_distance + new_distance_to_previous + new_distance_to_next

    def __calculate_time_in_rewrite( self, path: int, position: int, v: Vertice ):
        previous = self.paths[ path ][ position-1 ]
        middle   = self.paths[ path ][ position ]
        next     = self.paths[ path ][ position+1 ]
        old_dist_to_previous = calculate_distance( previous, middle )
        old_dist_to_next     = calculate_distance( middle, next )
        new_dist_to_previous = calculate_distance( previous, v )
        new_dist_to_next     = calculate_distance( v, next )
        return self.path_times[ path ] - old_dist_to_previous - old_dist_to_next + new_dist_to_previous + new_dist_to_next
    
    def __calculate_time_in_remove( self, path: int, position: int ):
        previous = self.paths[ path ][ position-1 ]
        middle   = self.paths[ path ][ position ]
        next     = self.paths[ path ][ position+1 ]
        old_distance_to_previous = calculate_distance( previous, middle )
        old_distance_to_next     = calculate_distance( middle, next )
        new_distance             = calculate_distance( previous, next )
        return self.path_times[ path ] - old_distance_to_previous - old_distance_to_next + new_distance
    
    def __recalculate_time( self, path: int ):
        sum = 0.0
        for i in range( len( self.paths[ path ] ) - 1 ):
            sum += calculate_distance( self.paths[ path ][ i ], self.paths[ path ][ i+1 ] )
        return sum
    
    def __check_if_vertice_is_used( self, vertice_for_check: Vertice ):
        for path in self.paths:
            for vertice in path:
                if vertice_for_check.equals( vertice ):
                    return True
        return False
    
    def __check_if_path_is_valid( self, path: int ):
        if path < 0 or path >= len( self.paths ):
            raise Exception("index of path is invalid")
    
    def __check_if_path_and_position_is_valid( self, path: int, position: int ):
        self.__check_if_path_is_valid( path )
        if position < 1 or position >= len( self.paths[ path ] ):
            raise Exception("index of position is invalid")
    
    def __check_if_position_is_initial_vertice( self, position: int ):
        return position == 0

    def __check_if_position_is_final_vertice( self, path: int, position: int ):
        size = len( self.paths[ path ] ) -1
        return position == size

    def add_initial_and_final_vertices( self, path: int, initial_vertice: Vertice, final_vertice: Vertice ):
        self.__check_if_path_is_valid( path )
        new_time = calculate_distance( initial_vertice, final_vertice )
        if self.time_per_path < new_time:
            raise Exception("Distance between initial and final vertice is bigger than time_per_paths")
        self.paths[ path ].append( initial_vertice )
        self.paths[ path ].append( final_vertice )
        self.path_times[ path ] = new_time
        self.total_time += new_time
    
    def add( self, path: int, vertice: Vertice ) -> bool:
        self.__check_if_path_is_valid( path )
        position = len( self.paths[ path ] ) - 1
        return self.add_in_position( path, position, vertice )
    
    def add_in_position( self, path: int, position: int, vertice: Vertice ) -> bool:
        self.__check_if_path_and_position_is_valid( path, position )
        if self.__check_if_vertice_is_used( vertice ) :
            return False
        if vertice == None :
            raise Exception("Vertice is None")
    
        new_time = self.__calculate_time_in_add( path, position, vertice )

        if( self.time_per_path >= new_time ):
            self.__update_reward_in_add( path, vertice )
            self.__add_in_path( path, position, vertice )
            self.__update_time( path, new_time )
            return True
    
        return False

    def rewrite( self, path, position, v ):
        if self.__check_if_path_and_position_is_valid( path, position ) :
            return False
        if self.__check_if_vertice_is_used( v ) :
            return False

        new_time = self.__calculate_time_in_rewrite( path, position, v )

        if self.time_per_path > new_time :
            self.__update_reward_in_rewrite( path, position, v )
            self.__remove_in_path( path, position )
            self.__add_in_path( path, position, v )
            self.__update_time( path, new_time )
            return True
    
        return False

    def swap( self, path, pos1, pos2 ):
        self.__check_if_path_and_position_is_valid( path, pos1 )
        self.__check_if_path_and_position_is_valid( path, pos2 )

        v = self.paths[ path ][ pos1 ]
        self.paths[ path ][ pos1 ] = self.paths[ path ][ pos2 ]
        self.paths[ path ][ pos2 ] = v

        new_time = self.__recalculate_time( path )

        if self.time_per_path > new_time :
            self.__update_time( path, new_time )
            return True
        else:
            v = self.paths[ path ][ pos1 ]
            self.paths[ path ][ pos1 ] = self.paths[ path ][ pos2 ]
            self.paths[ path ][ pos2 ] = v
            return False
    
    def swap( self, path1, position1, path2, position2 ):
        self.__check_if_path_and_position_is_valid( path1, position1 )
        self.__check_if_path_and_position_is_valid( path2, position2 )
        if( self.__check_if_position_is_initial_vertice( position1 ) or self.__check_if_position_is_final_vertice( path1, position1 ) ):
            raise Exception("do not swap initial or final vertice")
        if( self.__check_if_position_is_initial_vertice( position2 ) or self.__check_if_position_is_final_vertice( path2, position2 )):
            raise Exception("do not swap initial or final vertice")

        reward_1 = self.paths[ path1 ][ position1 ].get_reward()
        reward_2 = self.paths[ path2 ][ position2 ].get_reward()

        v = self.paths[ path1 ][ position1 ]
        self.paths[ path1 ][ position1 ] = self.paths[ path2 ][ position2 ]
        self.paths[ path2 ][ position2 ] = v

        new_time_path_1 = self.__recalculate_time( path1 )
        new_time_path_2 = self.__recalculate_time( path2 )

        if( (self.time_per_path > new_time_path_1 and self.time_per_path > new_time_path_2) ):
            self.__update_time( path1, new_time_path_1 )
            self.__update_time( path2, new_time_path_2 )
            self.path_rewards[ path1 ] += reward_2 - reward_1
            self.path_rewards[ path2 ] += reward_1 - reward_2
            return True
        else:
            v = self.paths[ path1 ][ position1 ]
            self.paths[ path1 ][ position1 ] = self.paths[ path2 ][ position2 ]
            self.paths[ path2 ][ position2 ] = v
            return False

    def remove( self, path, position ):
        if( self.__check_if_path_and_position_is_valid( path, position ) ):
            return False
        self.__update_reward_in_remove( path, position )
        new_time = self.__calculate_time_in_remove( path, position )
        self.__update_time( path, new_time )
        self.__remove_in_path( path, position )
        return True
    
    def move( self, path1: int, position1: int, path2: int, position2: int ):
        self.__check_if_path_and_position_is_valid( path1, position1 )
        self.__check_if_path_and_position_is_valid( path2, position2 )

        v = self.paths[ path1 ][ position1 ]

        new_time_path_1 = self.__calculate_time_in_remove( path1, position1 )
        new_time_path_2 = self.__calculate_time_in_add( path2, position2, v )

        if( self.time_per_path > new_time_path_2 ):
            self.__update_time( path1, new_time_path_1 )
            self.__update_time( path2, new_time_path_2 )
            self.__update_reward_in_remove( path1, position1 )
            self.__remove_in_path( path1, position1 )
            self.__update_reward_in_add( path2, v )
            self.__add_in_path( path2, position2, v )
            return True
        
        return False
    
    def is_empty( self, path ):
        if( self.__check_if_path_is_valid( path ) ):
            return False
        return len( self.paths[ path ] ) == 2
    
    def get_last_path_vertice_in_path( self, path ):
        if( self.__check_if_path_is_valid( path ) ):
            return None
        last_position = len( self.paths[ path ] ) - 1 - 1
        return self.paths[ path ][ last_position ]
    
    def get_vertice_in_path( self, path, position ):
        if( self.__check_if_path_and_position_is_valid( path, position ) ):
            return None
        return self.paths[ path ][ position ]
    
    def get_rewards( self, path ):
        if( not self.__check_if_path_is_valid( path ) ):
            return self.path_rewards[ path ]
    
    def get_total_rewards( self ):
        return self.total_rewards
    
    def get_total_time( self ):
        return self.total_time
    
    def get_distance( self, path, position ):
        if( self.__check_if_path_and_position_is_valid( path, position ) ):
            return -1.0
        if( len( self.paths[ path ] ) == 2 ):
            return -1.0
        distance = calculate_distance( self.paths[ path ][ position-1 ], self.paths[ path ][ position ] )
        distance += calculate_distance( self.paths[ path ][ position ], self.paths[ path ][ position+1 ] )
        return distance
    
    def get_time_path( self, path ):
        if( self.__check_if_path_is_valid( path ) ):
            return -1.0
        return self.path_times[ path ]

    def get_time_per_path( self ):
        return self.time_per_path
    
    def get_number_paths( self ):
        return len( self.paths )

    def get_length_of_path( self, path ):
        self.__check_if_path_is_valid( path )
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