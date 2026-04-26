import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if -literal not in c], new_assignment):
                return True
            return False
        pure_literal = next((l for l, count in defaultdict(int, (l for clause in clauses for l in clause)).items() if count == len(clauses)), None)
        if pure_literal:
            literal = pure_literal
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if -literal not in c], new_assignment):
                return True
            return False
        literal = random.choice(clauses[0])
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if -literal not in c], new_assignment):
            return True
        return False
    
    def generate_random_3sat(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [-v for v in variables], 3)
            clauses.append(clause)
        return clauses
    
    def incidence_matrix(clauses, variables):
        matrix = [[0] * len(variables) for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal > 0:
                    matrix[i][literal - 1] = 1
                else:
                    matrix[i][-literal - 1] = 1
        return matrix
    
    def max_eigenvalue(matrix):
        n = len(matrix)
        eigenvalues = []
        for _ in range(n):
            v = [random.random() for _ in range(n)]
            v /= math.sqrt(sum(x * x for x in v))
            while True:
                Av = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
                lambda_v = sum(Av[i] * v[i] for i in range(n))
                if abs(lambda_v - max_eigenvalue) < 1e-6:
                    break
                v = Av
            eigenvalues.append(max_eigenvalue)
        return max(eigenvalues)
    
    n = random.choice([5, 8, 11, 14])
    m = random.randint(3 * n, 5 * n)
    clauses = generate_random_3sat(n, m)
    incidence_mat = incidence_matrix(clauses, list(range(1, n + 1)))
    max_lambda = max_eigenvalue(incidence_mat)
    
    assignment = {}
    depth = dpll(clauses, assignment)
    
    return {
        "metric_name": "DPLL Depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": depth == math.isclose(depth, max_lambda),
        "counterexample": "" if depth == math.isclose(depth, max_lambda) else f"Depth {depth} != λ_max {max_lambda}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    total_depth = 0
    total_count = 0
    
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        total_depth += result["metric_value"]
        total_count += result["instances_tested"]
        
        print(f"TRIAL: {result}")
    
    mean_depth = total_depth / total_count
    std_depth = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing]['counterexample']}\" first_failing_seed={seeds[first_failing]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")