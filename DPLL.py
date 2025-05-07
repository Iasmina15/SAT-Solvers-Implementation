def one_literal(clauses):
    unit_found = True
    while unit_found:
        unit_found = False
        for clause in clauses:
            if len(clause) == 1: #Found a single literal in a clause
                lit = clause[0] #We get the literal
                comp = "-" + lit if lit[0] != '-' else lit[1:] #Compute the complement
                clauses = [c for c in clauses if lit not in c] #Eliminate all clauses where the literal appears
                clauses = [[l for l in c if l != comp] for c in clauses] #Eliminate the complement from all clauses where it appears
                unit_found = True
                break #Loop until we don`t have any clauses with only one literal`
    return clauses


def pure_literal(clauses):
    literals = {lit for clause in clauses for lit in clause} #We get all literals

    def complement(lit):
        return "-" + lit if lit[0] != '-' else lit[1:] #Compute the complement

    pure_literals = {lit for lit in literals if complement(lit) not in literals} #Check for pure literals

    clauses = [clause for clause in clauses if not any(lit in pure_literals for lit in clause)] #Eliminate all clauses that contain the pure literal
    return clauses


def splitting(clauses):
    counts = []
    literals = []
    #From here we count how many times each literal appears through the clauses
    for clause in clauses:
        for lit in clause:
            if lit in literals:
                i = literals.index(lit)
                counts[i] += 1
            else:
                literals.append(lit)
                counts.append(1)
    if not literals:
        return None
    max_index = 0
    for i in range(1, len(counts)):
        if counts[i] > counts[max_index]:
            max_index = i 
    return literals[max_index] #We return the literal that has the most appearances

def dpll(clauses):
    clauses = one_literal(clauses) #Apply one_literal rule
    clauses = pure_literal(clauses) #Apply pure_literal rule

    if not clauses:
        return True #If the clause set is empty -> SATISFIABLE
    for clause in clauses:
        if len(clause) == 0:
            return False #If we have any clause that is empty in the set -> UNSATISFIABLE

    lit = splitting(clauses) #Apply slitting rule
    if lit is None:
        return False
    comp = "-" + lit if lit[0] != '-' else lit[1:] #Compute the complement
    
    #We assume the literal we split on is true
    pos = [c for c in clauses if lit not in c] #Eliminate all clauses where the literal appears
    pos = [[l for l in c if l != comp] for c in pos] #Eliminate the complement from all clauses
    if dpll(pos):
        return True #This branch turned SAT

    #Now, we attempt with false
    neg = [c for c in clauses if comp not in c] #Eliminate all clauses where the complement appears
    neg = [[l for l in c if l != lit] for c in neg] #Eliminate the literal from all clauses
    return dpll(neg)

print("Enter the formula in CNF form (e.g., A B, -A C, -B -C):")
user_input = input("Input: ")

clauses_str = user_input.split(',')

clauses = []
for clause in clauses_str:
    literals = clause.strip().split()  # Split clause into individual literals
    if literals:  # Skip empty clauses
        clauses.append(literals)

result = dpll(clauses)

if result:
    print("SATISFIABLE")
else:
    print("UNSATISFIABLE")
