from typing_extensions import final


class PathRelinking:
    def __init__(self, start_to_end: bool ) -> None:
        self.start_to_end = start_to_end
    
    def execute( self, start_solution, final_solution ):
        if self.start_to_end :
            actual = start_solution
            best = start_solution
            destiny = final_solution
        else:
            actual = final_solution
            best = final_solution
            destiny = start_solution

        for i in range( destiny.get_number_paths() ):
            for j in range( 1, destiny.get_length_of_path( i )-1 ):
                vertice = destiny.get_vertice_in_path( i, j )
                if j < actual.get_length_of_path( i )-1:
                    if actual.rewrite( i, j, vertice ) :
                        if best.get_total_rewards() < actual.get_total_rewards():
                            best = actual
                else:
                    if actual.add( i, vertice ):
                        if best.get_total_rewards() < actual.get_total_rewards():
                            best = actual
        return best