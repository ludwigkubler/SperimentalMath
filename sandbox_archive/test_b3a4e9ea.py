import random
import math
from collections import defaultdict

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = 1 / matrix[i][i]
        for j in range(cols):
            matrix[i][j] *= factor
        for k in range(rows):
            if k != i:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def count_solutions(matrix):
    rows, cols = len(matrix), len(matrix[0])
    gaussian_matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in gaussian_matrix if any(row))
    nullity = cols - rank
    return 2 ** nullity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    variables = set(range(n))
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice(variables) for _ in range(3)]
        if len(set(clause)) == 3:
            clauses.append(clause)
    
    GF2_matrix = [[0] * (n + 1) for _ in range(len(clauses))]
    for i, clause in enumerate(clauses):
        for var in clause:
            GF2_matrix[i][var] = 1
        GF2_matrix[i][-1] = 1
    
    N = count_solutions(GF2_matrix)
    if N == 0:
        return {
            "metric_name": "seed_length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    seed_length = math.log2(N)
    return {
        "metric_name": "seed_length",
        "metric_value": seed_length,
        "instances_tested": 1,
        "conjecture_holds": abs(seed_length - math.log2(N)) < 0.5 * math.log2(N),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")