from Resolution import resolution #Imported the resolution algorithm already implemented

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


def davis_putnam(clauses):
    clauses = one_literal(clauses)
    clauses = pure_literal(clauses)
    
    new_clauses = resolution(clauses)
    
    if not new_clauses:  #No clauses are left
        return True  #-> SATISFIABLE
    
    if any(len(clause) == 0 for clause in new_clauses):  #An empty clause exists
        return False  #-> UNSATISFIABLE
    
    return davis_putnam(new_clauses)


print("Enter the formula in CNF form (e.g., A B, -A C, -B -C):")
user_input = input("Input: ")

clauses_str = user_input.split(',')

clauses = []

for clause in clauses_str:
    literals = clause.strip().split()
    clauses.append(literals)

result = davis_putnam(clauses)

if result:
    print("SATISFIABLE")
else:
    print("UNSATISFIABLE")
