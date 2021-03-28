#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
		 
		 
var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def check_FC(constraint, var):
    '''FCCheck from lecture'''
    val_list = []
    pruned = []
    domain_wipeout = True #True if no domain wipeout

    scope = constraint.get_scope() #get list of variables the constraint is over
    for k in range(len(scope)): #create a list storing the values of the variables in order
        val_list.append(scope[k].get_assigned_value())
        if val_list[k] == None: #store the index of the unassigned variable
            uninstantiated_var = k

    for d in var.cur_domain():
        val_list[uninstantiated_var] = d #change the unassigned variable value to d 
        if not constraint.check(val_list): #check if the value list satisfies all the constraints
            pruned.append((var, d))
            var.prune_value(d)
    if not var.cur_domain():
        domain_wipeout = False
    
    return (domain_wipeout, pruned)

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
    #IMPLEMENT
    if newVar == None:
        cons = csp.get_all_cons()
    else:
        cons = csp.get_cons_with_var(newVar)
    pruned = []
    dwo = True

    for c in cons:
        if c.get_n_unasgn() == 1:
            dwo, pruned_val = check_FC(c, c.get_unasgn_vars()[0])
            pruned += pruned_val
            if not dwo:
                break
    
    return (dwo, pruned)

'''
def enforce_GAC(queue, cons):
    pruned = []
    while queue:
        c = queue.pop(0) #left first
        for var in cons.get_scope():
            for d in var.cur_dom():
                if not cons.has_support(var, d): #if assignment not found
                    var.prune_value(d) #remove d from the domain of V
                    pruned.append(d)
                    if not var.cur_dom():
                        queue.clear()
                        return (False, pruned)
                    else:
'''

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT
    if newVar == None:
        cons = csp.get_all_cons()
    else:
        cons = csp.get_cons_with_var(newVar)
    queue = cons.copy() #create copy of constraint list
    dwo = []
    pruned = []

    while queue:
        c = queue.pop(0) #left first
        for var in c.get_scope():
            for d in var.cur_domain():
                if not c.has_support(var, d): #if assignment not found
                    pruned.append((var,d))
                    var.prune_value(d) #remove d from the domain of V
                    if not var.cur_domain():
                        queue.clear()
                        return (False, pruned)
                    else:
                        for con in cons:
                            if var in con.get_scope() and \
                                con not in queue:
                                queue.append(con)
    
    return (True, pruned)

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    #IMPLEMENT
    variable_list = csp.get_all_unasgn_vars()
    mrv = None
    for variable in variable_list:
        if not mrv:
            mrv = variable
        else:
            if variable.cur_domain_size() < mrv.cur_domain_size():
                mrv = variable
    
    return mrv
	