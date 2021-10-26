from Solution import Solution
from ScorePoint import ScorePoint
from Instance import Instance
from Utils import calculate_distance, find_min_max
from random import random

class RandomGreedyGen_MinMax:
    def __init__( self, alpha, margin, number_paths, time_per_path, instance ):
        self.alpha = alpha
        self.margin = margin
        self.number_paths = number_paths
        self.time_per_path = time_per_path
        self.instance = instance
        self.unused_vertices = []

    def initialize_solution( self, number_paths, time_per_path, initial_vertice, final_vertice ):
        sol = Solution( number_paths, time_per_path )
        for i in range( number_paths ):
            sol.add_initial_and_final_vertices( i, initial_vertice, final_vertice )
        return sol
    
    def get_scores( self, vertices ):
        scores = []
        for v in vertices:
            scores.append( v.get_reward() )
        return scores
    
    def get_distances( self, scores_points ):
        distances = []
        for sp in scores_points:
            distances.append( sp.distance )
        return distances
    
    def calcule_probability( self, actual_vertice, vertices ):
        min_reward = 0.0
        max_reward = 0.0
        min_distance = 0.0
        max_distance = 0.0
        sum_values = 0.0
        n_vertices = len( vertices )
        score_points = []

        if n_vertices == 0:
            return score_points
        
        for v in vertices:
            s = ScorePoint()
            s.p = v
            s.distance = calculate_distance( actual_vertice, v )
            score_points.append( s )
        
        min_reward, max_reward = find_min_max( self.get_scores( vertices ) )
        min_distance, max_distance = find_min_max( self.get_distances( score_points ) )

        for i in range( n_vertices ):
            score_points[ i ].score_reward = self.calcule_score( score_points[ i ].p.get_reward(), min_reward, max_reward )
            score_points[ i ].distance = self.calcule_score( score_points[ i ].distance, min_distance, max_distance )
            score_points[ i ].value = 1.1 + score_points[ i ].score_reward - score_points[ i ].score_distance
            sum_values += score_points[ i ].value
        
        for i in range( n_vertices ):
            score_points[ i ].probability = score_points[ i ].value / sum_values
        
        return score_points
    
    def select_vertice_greedy( self, score_points ):
        selected_position = 0
        max = 0.0
        for i in range( len( score_points ) ):
            if max < score_points[ i ].probability :
                max = score_points[ i ].probability
                selected_position = i
        return selected_position
    
    def select_vertice_random( self, score_points ):
        selected_position = -1
        random_number = random()
        sum = 0.0
        for i in range( len( score_points ) ):
            sum += score_points[ i ].probability
            if random_number < sum:
                selected_position = i
                break
        return selected_position
    
    def select_vertice( self, score_points ):
        if len( score_points ) == 0:
            return -1
        is_greedy = random() >= self.alpha
        if is_greedy:
            return self.select_vertice_greedy( score_points )
        return self.select_vertice_random( score_points )
        
    def calcule_score( self, value, min, max ):
        return (value - min)/(max - min)

    def generate( self, vertices ):
        is_added = True
        sol = self.initialize_solution( self.number_paths, self.time_per_path, self.instance.get_initial_vertice(), self.instance.get_final_vertice() )
        sol.update_time_per_path( self.margin * sol.get_time_per_path() )
        self.unused_vertices = vertices

        while is_added:
            is_added = False
            for i in range( self.number_paths ):
                selected_index = self.select_vertice( self.calcule_probability( sol.get_last_path_vertice_in_path( i ), self.unused_vertices ) )
                if selected_index == -1:
                    break
                selected_vertice = self.unused_vertices[ selected_index ]
                print( selected_index )
                print( selected_vertice.to_string() )
                if sol.add( i, selected_vertice ):
                    is_added = True
                    self.unused_vertices.remove( selected_vertice )
                    print("adicionou")
        
        return sol
    
    def get_unused_vertices(self):
        return self.unused_vertices