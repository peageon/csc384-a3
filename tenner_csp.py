#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools

def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.
       
       
       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board
    
       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       
       
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''
    #name Variable and Constraints like vars.append(Variable('Q{}'.format(i), dom))
    board, sum_list = initial_tenner_board
    var_list = []
    constraints = []
    #create list of variable with corresponding domains
    for i in range(len(board)): #for each row i of the board
      row_var = []
      domain = [k for k in range(10)] #create domain list
      for j in range(len(board[i])): #remove used domains
        if board[i][j] != -1:
          domain.remove(board[i][j])
      for j in range(len(board[i])): #add variables to var_list
        if board[i][j] != -1:
          V = Variable('V{}{}'.format(i,j), [board[i][j]])
          V.assign(board[i][j])
          row_var.append(V)
        else:
          row_var.append(Variable('V{}{}'.format(i,j), domain))
      var_list.append(row_var)
    #We have created a list of list of variables in each row
    #Now we have to add the constraints

    #constraint format 
    #    Constraint("C(Q{},Q{})".format(qi+1,qj+1),[vars[qi], vars[qj]])
    for row in range(len(board)): # for each row
      for i in range(len(board[row])):
        #BINARY NOT-EQUAL CONSTRAINTS | ROW CONSTRAINT
        for j in range(i+1, len(board[row])):
          con = Constraint("C(R{},R{})".format(i,j), [var_list[row][i],var_list[row][j]])
          #create list of satisfying tuples
          sat_tup = [(x,y) for x in var_list[row][i].domain() for y in var_list[row][j].domain() if x != y]
          con.add_satisfying_tuples(sat_tup) #add satisfying tuples
          constraints.append(con) #add constraint to constraint list
        
        #ADJACENT VERTICAL CONSTRAINT
        if row < len(board) - 1:
          con = Constraint("C(ADV{},ADV{})".format(i,j), [var_list[row][i], var_list[row+1][i]])
          sat_tup = [(x,y) for x in var_list[row][i].domain() for y in var_list[row+1][i].domain() if x != y]
          con.add_satisfying_tuples(sat_tup)
          constraints.append(con)
          #ADJACENT DIAGONAL RIGHT CONSTRAINT
          if i < len(board[row]) - 1:
            con = Constraint("C(ADD{},ADD{})".format(i,j), [var_list[row][i], var_list[row+1][i+1]])
            sat_tup = [(x,y) for x in var_list[row][i].domain() for y in var_list[row+1][i+1].domain() if x != y]
            con.add_satisfying_tuples(sat_tup)
            constraints.append(con)
          #ADJACENT DIAGONAL LEFT CONSTRAINT
          if 0 < i:
            con = Constraint("C(ADD{},ADD{})".format(i,j), [var_list[row][i], var_list[row+1][i-1]])
            sat_tup = [(x,y) for x in var_list[row][i].domain() for y in var_list[row+1][i-1].domain() if x != y]
            con.add_satisfying_tuples(sat_tup)
            constraints.append(con)
    #SUM CONSTRAINT
    for col in range(len(board[row])):
      col_vars = [var_list[i][col] for i in range(len(board))]
      con = Constraint("C(Col{})".format(col), col_vars)
      domains = [var_list[i][col].domain() for i in range(len(board))]
      #cartesian product using itertools
      sat_tup = []
      for combination in itertools.product(*domains):
        if sum(combination) == sum_list[col]:
          sat_tup.append(combination)
      con.add_satisfying_tuples(sat_tup)
      constraints.append(con)
    csp_model = CSP("Tenner_Model_1", [var_list[i][j] for i in range(len(board)) for j in range(len(board[0]))])
    for con in constraints:
      csp_model.add_constraint(con)
    return csp_model, var_list

      
          
##############################

def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.
    
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular, instead
       of binary non-equals constaints model_2 has a combination of n-nary 
       all-different constraints: all-different constraints for the variables in
       each row, and sum constraints for each column. You may use binary 
       contstraints to encode contiguous cells (including diagonally contiguous 
       cells), however. Each -ary constraint is over more 
       than two variables (some of these variables will have
       a single value in their domain). model_2 should create these
       all-different constraints between the relevant variables.
    '''

#IMPLEMENT
    return None, None #CHANGE THIS
