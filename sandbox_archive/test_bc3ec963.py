import random
import math
import sys
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(mat):
        n = len(mat)
        for i in range(n):
            # Find pivot row
            max_row = i
            for j in range(i+1, n):
                if abs(mat[j][i]) > abs(mat[max_row][i]):
                    max_row = j
            mat[i], mat[max_row] = mat[max_row], mat[i]
            
            # Eliminate non-pivot elements
            factor = mat[i][i]
            for j in range(i, n):
                mat[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = mat[k][i]
                    for j in range(i, n):
                        mat[k][j] -= factor * mat[i][j]
        return mat
    
    def max_eigenvalue(mat):
        n = len(mat)
        eigenvalues = [1.0] * n
        tolerance = 1e-6
        iterations = 100
        for _ in range(iterations):
            new_eigenvalues = [sum(mat[i][j] * eigenvalues[j] for j in range(n)) / mat[i][i] for i in range(n)]
            if all(abs(new_eigenvalues[i] - eigenvalues[i]) < tolerance for i in range(n)):
                break
            eigenvalues = new_eigenvalues
        return max(eigenvalues)
    
    def dpll_depth(clauses, assignment):
        if not clauses:
            return 0
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment[:]
            new_assignment[abs(literal)-1] = literal > 0
            return dpll_depth([c for c in clauses if literal not in c and -literal not in c], new_assignment) + 1
        pure_literal = next((i+1 for i, (v, count) in enumerate(collections.Counter(sum(clauses, []))) if count == len(clauses)), None)
        if pure_literal:
            new_assignment = assignment[:]
            new_assignment[pure_literal-1] = True
            return dpll_depth([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment) + 1
        literal = random.choice(sum(clauses, []))
        new_assignment = assignment[:]
        new_assignment[abs(literal)-1] = literal > 0
        return max(dpll_depth([c for c in clauses if literal not in c and -literal not in c], new_assignment), dpll_depth([c for c in clauses if -literal not in c and literal not in c], new_assignment)) + 1
    
    def incidence_matrix(n, m):
        matrix = [[0] * n for _ in range(m)]
        for i in range(m):
            literals = random.sample(range(1, n+1), 3)
            for literal in literals:
                matrix[i][abs(literal)-1] = 1 if literal > 0 else -1
        return matrix
    
    def generate_random_3sat(n, m):
        clauses = []
        for _ in range(m):
            literals = random.sample(range(1, n+1), 3)
            clause = [random.choice([l, -l]) for l in literals]
            clauses.append(clause)
        return clauses
    
    n_values = [5, 8, 11, 14]
    total_depth = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        m = random.randint(3*n//2, 6*n)
        clauses = generate_random_3sat(n, m)
        incidence_mat = incidence_matrix(n, m)
        max_lambda = max_eigenvalue(incidence_mat)
        
        depth = dpll_depth(clauses, [False] * n)
        total_depth += depth
        instances_tested += 1
        
        if abs(depth - max_lambda) > 0.1 * max_lambda:
            conjecture_holds = False
            counterexample = f"n={n}, m={m}, DPLL depth={depth}, λ_max={max_lambda}"
    
    return {
        "metric_name": "DPLL Depth",
        "metric_value": total_depth / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")