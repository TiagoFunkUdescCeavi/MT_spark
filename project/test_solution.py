from Solution import Solution
from Vertice import Vertice
import unittest

class test_solution( unittest.TestCase ):
    def test_init( self ):
        sol = Solution( 2, 7.5 )
        self.assertAlmostEqual( sol.get_number_paths(), 2 )
        self.assertAlmostEqual( sol.get_time_per_path(), 7.5 )
        self.assertAlmostEqual( sol.get_total_rewards(), 0.0 )
        self.assertAlmostEqual( sol.get_total_time(), 0.0 )
        self.assertAlmostEqual( sol.get_rewards( 0 ), 0.0 )
        self.assertAlmostEqual( sol.get_rewards( 1 ), 0.0 )
        self.assertAlmostEqual( sol.get_time_path( 0 ), 0.0 )
        self.assertAlmostEqual( sol.get_time_path( 1 ), 0.0 )
    
    def test_set_initial_and_final_vertices( self ):
        initial = Vertice( 0.0, 0.0, 0 )
        final = Vertice( 3.0, 4.0, 0 )
        sol = Solution( 2, 7.5 )
        for i in range( 2 ):
            sol.add_initial_and_final_vertices( i, initial, final )
        
        self.assertAlmostEqual( sol.get_number_paths(), 2 )
        self.assertAlmostEqual( sol.get_time_per_path(), 7.5 )
        self.assertAlmostEqual( sol.get_total_rewards(), 0.0 )
        self.assertAlmostEqual( sol.get_total_time(), 10.0 )
        for i in range( 2 ):
            self.assertAlmostEqual( sol.get_length_of_path( i ), 2 )
            self.assertAlmostEqual( sol.get_time_path( i ), 5.0 )
            self.assertAlmostEqual( sol.get_rewards( i ), 0 )
    
    def test_set_invalid_initial_and_final_vertices( self ):
        initial = Vertice( 0.0, 0.0, 0 )
        final = Vertice( 3.0, 4.0, 0 )
        sol = Solution( 2, 7.5 )

        self.assertRaises( Exception, sol.add_initial_and_final_vertices, -1, initial, final)
        self.assertRaises( Exception, sol.add_initial_and_final_vertices, 2, initial, final)
        self.assertRaises( Exception, sol.add_initial_and_final_vertices, 59, initial, final)
    
    def test_set_initial_and_final_vertices_with_invalid_length( self ):
        initial = Vertice( 0.0, -7.0, 0 )
        final = Vertice( 0.0, 7.0, 0 )
        sol = Solution( 2, 13.3 )

        self.assertRaises( Exception, sol.add_initial_and_final_vertices, 0, initial, final)
    
    def test_add( self ):
        initial = Vertice( 0.0, 0.0, 0 )
        final = Vertice ( 3.0, 4.0, 0 )
        new_vertice = Vertice( 6.0, 8.0, 5 )
        sol = Solution( 2, 15.0 )

        for i in range( 2 ):
            sol.add_initial_and_final_vertices( i, initial, final )
        
        self.assertAlmostEqual( sol.add( 0, new_vertice ), True )

        self.assertAlmostEqual( sol.get_length_of_path( 0 ), 3 )
        self.assertAlmostEqual( sol.get_time_path( 0 ), 15.0 )
        self.assertAlmostEqual( sol.get_rewards( 0 ), 5 )

        self.assertAlmostEqual( sol.get_length_of_path( 1 ), 2 )
        self.assertAlmostEqual( sol.get_time_path( 1 ), 5.0 )
        self.assertAlmostEqual( sol.get_rewards( 1 ), 0 )

        self.assertAlmostEqual( sol.get_number_paths(), 2 )
        self.assertAlmostEqual( sol.get_time_per_path(), 15.0 )
        self.assertAlmostEqual( sol.get_total_rewards(), 5.0 )
        self.assertAlmostEqual( sol.get_total_time(), 20.0 )

    def test_invalid_adds( self ):
        initial = Vertice( 0.0, 0.0, 0 )
        final = Vertice ( 3.0, 4.0, 0 )
        new_vertice = Vertice( 6.0, 8.0, 5 )
        sol = Solution( 2, 7.5 )

        for i in range( 2 ):
            sol.add_initial_and_final_vertices( i, initial, final )
        
        self.assertRaises( Exception, sol.add, -1, new_vertice )
        self.assertRaises( Exception, sol.add, 2, new_vertice )
        self.assertRaises( Exception, sol.add, 1, None )
        self.assertAlmostEqual( sol.add( 1, new_vertice ), False )
    
    def test_add_with_repeated_vertice( self ):
        initial = Vertice( 0.0, 0.0, 0 )
        final = Vertice ( 3.0, 4.0, 0 )
        new_vertice = Vertice( 6.0, 8.0, 5 )
        other_vertice = Vertice( 1.0, 2.0, 5.0 )
        sol = Solution( 2, 25.0 )

        for i in range( 2 ):
            sol.add_initial_and_final_vertices( i, initial, final )
        
        self.assertAlmostEqual( sol.add( 0, new_vertice ), True )

        self.assertAlmostEqual( sol.add( 0, new_vertice ), False )
        self.assertAlmostEqual( sol.add( 1, new_vertice ), False )

        self.assertAlmostEqual( sol.add( 0, other_vertice), True )

    
    def test_move( self ):
        initial = Vertice( 1.0, 1.0, 0 )
        final = Vertice( 2.0, 2.0, 0 )
        v1 = Vertice( 2.3, 4.5, 1 )
        v2 = Vertice( 1.8, 2.1, 2 )
        v3 = Vertice( 2.2, 3.3, 4 )
        v4 = Vertice( 2.7, 3.1, 8 )
        sol = Solution( 2, 9.0 )

        for i in range( 2 ):
            sol.add_initial_and_final_vertices( i, initial, final )

        sol.add( 0, v1 )
        sol.add( 0, v2 )
        sol.add( 1, v3 )
        sol.add( 1, v4 )

        self.assertAlmostEqual( sol.move( 1,2,0,3 ), True )

        self.assertAlmostEqual( sol.get_length_of_path( 0 ), 5 )
        self.assertAlmostEqual( sol.get_time_path( 0 ), 8.8344, places=4 )
        self.assertAlmostEqual( sol.get_rewards( 0 ), 11 )

        self.assertAlmostEqual( sol.get_length_of_path( 1 ), 3 )
        self.assertAlmostEqual( sol.get_time_path( 1 ), 3.9095, places=4 )
        self.assertAlmostEqual( sol.get_rewards( 1 ), 4 )

        self.assertAlmostEqual( sol.get_number_paths(), 2 )
        self.assertAlmostEqual( sol.get_time_per_path(), 9.0 )
        self.assertAlmostEqual( sol.get_total_rewards(), 15.0 )
        self.assertAlmostEqual( sol.get_total_time(), 12.7439, places=4 )

    def test_invalid_move( self ):
        initial = Vertice( 1.0, 1.0, 0 )
        final = Vertice( 2.0, 2.0, 0 )
        v1 = Vertice( 2.3, 4.5, 1 )
        v2 = Vertice( 1.8, 2.1, 2 )
        v3 = Vertice( 2.2, 3.3, 4 )
        v4 = Vertice( 2.7, 3.1, 8 )
        sol = Solution( 2, 7.0 )

        for i in range( 2 ):
            sol.add_initial_and_final_vertices( i, initial, final )

        sol.add( 0, v1 )
        sol.add( 0, v2 )
        sol.add( 1, v3 )
        sol.add( 1, v4 )

        self.assertAlmostEqual( sol.move( 1,2,0,3 ), False )

        self.assertAlmostEqual( sol.get_length_of_path( 0 ), 4 )
        self.assertAlmostEqual( sol.get_time_path( 0 ), 6.4088, places=4 )
        self.assertAlmostEqual( sol.get_rewards( 0 ), 3 )

        self.assertAlmostEqual( sol.get_length_of_path( 1 ), 4 )
        self.assertAlmostEqual( sol.get_time_path( 1 ), 4.4366, places=4 )
        self.assertAlmostEqual( sol.get_rewards( 1 ), 12 )

        self.assertAlmostEqual( sol.get_number_paths(), 2 )
        self.assertAlmostEqual( sol.get_time_per_path(), 7.0 )
        self.assertAlmostEqual( sol.get_total_rewards(), 15.0 )
        self.assertAlmostEqual( sol.get_total_time(), 10.8453, places=4 )
    
    def test_invalid_position_on_move( self ):
        initial = Vertice( 1.0, 1.0, 0 )
        final = Vertice( 2.0, 2.0, 0 )
        v1 = Vertice( 2.3, 4.5, 1 )
        v2 = Vertice( 1.8, 2.1, 2 )
        v3 = Vertice( 2.2, 3.3, 4 )
        v4 = Vertice( 2.7, 3.1, 8 )
        sol = Solution( 2, 7.0 )

        for i in range( 2 ):
            sol.add_initial_and_final_vertices( i, initial, final )
        
        sol.add( 0, v1 )
        sol.add( 0, v2 )
        sol.add( 1, v3 )
        sol.add( 1, v4 )

        self.assertRaises( Exception, sol.move, 1, 2, 0, 4 )
        self.assertRaises( Exception, sol.move, 1, 0, 0, 3 )
        self.assertRaises( Exception, sol.move, 1, -2, 0, 3 )
    
    def test_swap( self ):
        initial = Vertice( 1.0, 1.0, 0 )
        final = Vertice( 2.0, 2.0, 0 )
        v1 = Vertice( 2.3, 4.5, 1 )
        v2 = Vertice( 1.8, 2.1, 2 )
        v3 = Vertice( 2.2, 3.3, 4 )
        v4 = Vertice( 2.7, 3.1, 8 )
        sol = Solution( 2, 7.0 )

        for i in range( 2 ):
            sol.add_initial_and_final_vertices( i, initial, final )
        
        sol.add( 0, v1 )
        sol.add( 0, v2 )
        sol.add( 1, v3 )
        sol.add( 1, v4 )

        self.assertAlmostEqual( sol.swap( 1, 2, 0, 1 ), True )

        self.assertAlmostEqual( sol.get_length_of_path( 0 ), 4 )
        self.assertAlmostEqual( sol.get_time_path( 0 ), 4.2708, places=4 )
        self.assertAlmostEqual( sol.get_rewards( 0 ), 10 )

        self.assertAlmostEqual( sol.get_length_of_path( 1 ), 4 )
        self.assertAlmostEqual( sol.get_time_path( 1 ), 6.3163, places=4 )
        self.assertAlmostEqual( sol.get_rewards( 1 ), 5 )

        self.assertAlmostEqual( sol.get_number_paths(), 2 )
        self.assertAlmostEqual( sol.get_time_per_path(), 7.0 )
        self.assertAlmostEqual( sol.get_total_rewards(), 15.0 )
        self.assertAlmostEqual( sol.get_total_time(), 10.5871, places=4 )

    def test_invalid_move( self ):
        initial = Vertice( 1.0, 1.0, 0 )
        final = Vertice( 2.0, 2.0, 0 )
        v1 = Vertice( 2.3, 4.5, 1 )
        v2 = Vertice( 1.8, 2.1, 2 )
        v3 = Vertice( 2.2, 3.3, 4 )
        v4 = Vertice( 2.7, 3.1, 8 )
        sol = Solution( 2, 6.3 )

        for i in range( 2 ):
            sol.add_initial_and_final_vertices( i, initial, final )
        
        sol.add( 0, v1 )
        sol.add( 0, v2 )
        sol.add( 1, v3 )
        sol.add( 1, v4 )

        self.assertAlmostEqual( sol.swap( 1, 2, 0, 1 ), False )
    
    def test_invalid_position_on_swap( self ):
        initial = Vertice( 1.0, 1.0, 0 )
        final = Vertice( 2.0, 2.0, 0 )
        v1 = Vertice( 2.3, 4.5, 1 )
        v2 = Vertice( 1.8, 2.1, 2 )
        v3 = Vertice( 2.2, 3.3, 4 )
        v4 = Vertice( 2.7, 3.1, 8 )
        sol = Solution( 2, 7.0 )

        for i in range( 2 ):
            sol.add_initial_and_final_vertices( i, initial, final )
        
        sol.add( 0, v1 )
        sol.add( 0, v2 )
        sol.add( 1, v3 )
        sol.add( 1, v4 )
        
        self.assertRaises( Exception, sol.swap, 1, 2, 0, 3 )
        self.assertRaises( Exception, sol.swap, 1, 0, 0, 3 )
        self.assertRaises( Exception, sol.swap, 1, -2, 0, 3 )
    
    def test_swap_before_final_vertice( self ):
        initial = Vertice( 1.0, 1.0, 0 )
        final = Vertice( 2.0, 2.0, 0 )
        v1 = Vertice( 2.3, 4.5, 1 )
        sol = Solution( 2, 7.0 )

        for i in range( 2 ):
            sol.add_initial_and_final_vertices( i, initial, final )
        
        sol.add( 0, v1 )
        
        self.assertRaises( Exception, sol.swap, 0, 1, 1, 1 )
