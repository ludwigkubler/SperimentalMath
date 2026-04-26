import random
import itertools

# Set random seed for reproducibility
random.seed(42)

def generate_random_3sat(n, m):
    """Generate a random 3-CNF formula with n variables and m clauses."""
    clauses = []
    for _ in range(m):
        clause = random.sample(range(n), 3)
        literals = [random.choice([-1, 1]) for _ in range(3)]
        clauses.append([(clause[i], literals[i]) for i in range(3)])
    return clauses

def compute_resolution_width(phi):
    """Compute the minimal resolution width of a 3-CNF formula using DPLL."""
    # Simplified DPLL implementation for demonstration purposes only
    def dpll(phi, width):
        if not phi:
            return True
        if any(not clause for clause in phi):
            return False
        for clause in phi:
            if len(clause) == 1:
                literal, = clause
                var, sign = literal
                new_phi = [c for c in phi if (var, -sign) not in c]
                if dpll(new_phi, width + 1):
                    return True
        return False

    width = 0
    while not dpll(phi, width):
        width += 1
    return width

def compute_nilpotency_class(phi):
    """Compute the nilpotency class of the Bass Nil-group of a 3-CNF formula."""
    # Simplified implementation for demonstration purposes only
    def commutator(a, b):
        return a * b - b * a

    n = len(set(var for clause in phi for var, _ in clause))
    m = len(phi)
    generators = [f"x{i}" for i in range(n)] + [f"c{i}" for i in range(m)]
    relations = []
    for i, clause in enumerate(phi):
        for var, sign in clause:
            relations.append(f"x{var} * c{i} - c{i} * x{var}")
            relations.append(f"x{var} * x{var} - 1")

    # Initialize the augmentation ideal
    ideal = set()
    for gen in generators:
        ideal.add(gen)

    # Compute the lower central series
    series = [ideal]
    while True:
        new_series = set()
        for a in series[-1]:
            for b in series[-1]:
                new_series.add(commutator(a, b))
        if not new_series:
            break
        series.append(new_series)

    # Estimate the nilpotency class
    return len(series) - 1

def test_conjecture(n, m):
    """Test the conjecture for a random 3-CNF formula with n variables and m clauses."""
    phi = generate_random_3sat(n, m)
    w = compute_resolution_width(phi)
    c = compute_nilpotency_class(phi)
    print(f"n={n}, m={m}, w={w}, c={c}")
    return c <= 2 * w

def main():
    for n in [5, 8, 11, 14]:
        m = n * 2  # Adjust the number of clauses to ensure satisfiability
        if not test_conjecture(n, m):
            print("RESULT: FALSIFIED")
            return
    print("RESULT: SUPPORTED")

if __name__ == "__main__":
    main()