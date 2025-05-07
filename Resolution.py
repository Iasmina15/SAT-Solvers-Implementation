def negate(literal):
    if literal[0] == "-":
        return literal[1:] # If literal is "-A", it returns "A"
    else:
        return "-" + literal # If literal is "A", it returns "-A"
    
def is_complementary(lit1, lit2):
    return lit1 == negate(lit2) # Checks if two literals are complementary

def resolve(clause1, clause2):
    resolvents = []  # Stores new clauses
    for lit1 in clause1:
        for lit2 in clause2:
            if is_complementary(lit1, lit2):  # Complementary literals found
                new_clause = (clause1 - {lit1}) | (clause2 - {lit2}) # Create a new clause after removing the complementary literals
                resolvents.append(new_clause)  # Add the new clause
    return resolvents

def resolution(clauses):
    while True:
        new_clauses = []  # List to store newly resolved clauses
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):  
                resolvents = resolve(clauses[i], clauses[j]) # Resolve each pair of clauses 
                for new_clause in resolvents:
                    if not new_clause: # If the new clause is empty
                        return False # -> UNSATISFIABLE
                    if new_clause not in clauses and new_clause not in new_clauses:
                        new_clauses.append(new_clause)  # It adds the new clause only if it is not a duplicate

        if not new_clauses:  # If no new clauses were added
            return True  # -> SATISFIABLE

        clauses.extend(new_clauses)  # Add new clauses to the list

print("Enter the formula in CNF form (e.g., A B, -A C, -B -C):")
user_input = input("Input: ")

clauses_str = user_input.split(',')
clauses = []

# Convert each clause from string to set of literals
for clause in clauses_str:
    literals = set(clause.strip().split())
    clauses.append(literals)

result = resolution(clauses)

if result:
    print("SATISFIABLE")
else:
    print("UNSATISFIABLE")
