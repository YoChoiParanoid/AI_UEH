from constraint import Problem, AllDifferentConstraint

problem = Problem()

names = ['Steve', 'Matthew', 'Jack', 'Alfred']
pets = ['cat', 'dog', 'rabbit', 'hamster']  # đổi 'unknown' → hamster
colors = ['blue', 'black', 'red', 'green']
countries = ['Canada', 'USA', 'Australia', 'France']

positions = range(4)

for i in positions:
    problem.addVariable(f"name_{i}", names)
    problem.addVariable(f"pet_{i}", pets)
    problem.addVariable(f"color_{i}", colors)
    problem.addVariable(f"country_{i}", countries)

problem.addConstraint(AllDifferentConstraint(), [f"name_{i}" for i in positions])
problem.addConstraint(AllDifferentConstraint(), [f"pet_{i}" for i in positions])
problem.addConstraint(AllDifferentConstraint(), [f"color_{i}" for i in positions])
problem.addConstraint(AllDifferentConstraint(), [f"country_{i}" for i in positions])

# Define helper to bind two attributes at the same index
def bind(attr1, value1, attr2, value2):
    for i in positions:
        def constraint(a, b, v1=value1, v2=value2):
            return (a == v1 and b == v2) or (a != v1)
        problem.addConstraint(constraint, (f"{attr1}_{i}", f"{attr2}_{i}"))

# Add constraints
bind("name", "Steve", "color", "blue")           # Steve's car is blue
bind("pet", "cat", "country", "Canada")          # Person who has a cat lives in Canada
bind("name", "Matthew", "country", "USA")        # Matthew lives in USA
bind("color", "black", "country", "Australia")   # Black car → Australia
bind("name", "Jack", "pet", "cat")               # Jack has a cat
bind("name", "Alfred", "country", "Australia")   # Alfred → Australia
bind("pet", "dog", "country", "France")          # Dog → France

# Solve
solutions = problem.getSolutions()

if not solutions:
    print("No solution found.")
else:
    solution = solutions[0]
    print("\nHere are all the details:")
    print("\nName\t\tPet\t\tColor\t\tCountry")
    print("=" * 50)
    for i in positions:
        print(f"{solution[f'name_{i}']}\t\t{solution[f'pet_{i}']}\t\t{solution[f'color_{i}']}\t\t{solution[f'country_{i}']}")

    for i in positions:
        if solution[f"pet_{i}"] == "rabbit":
            print(f"\n\n✅ {solution[f'name_{i}']} is the owner of the rabbit!")
            break
