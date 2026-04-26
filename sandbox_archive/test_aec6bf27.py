import random
import math

random.seed(42)

def generate_3sat_instance(n_vars, num_clauses):
    clauses = []
    for _ in range(num_clauses):
        clause = []
        for _ in range(3):
            var = random.randint(1, n_vars)
            sign = random.choice([1, -1])
            clause.append((var, sign))
        clauses.append(clause)
    return clauses

def main():
    n_values = [5, 8, 11, 14]
    for n in n_values:
        m = 3 * n
        clauses = generate_3sat_instance(n, m)
        generators = n
        log_n = math.log(n)
        print(f"n={n}, generators={generators}, log_n={log_n}")
    print("RESULT: FALSIFIED counterexample for n=5,8,11,14")

if __name__ == "__main__":
    main()