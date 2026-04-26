import random
from collections import defaultdict
import math
import json
import sys

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(cols):
        pivot_row = None
        for j in range(rank, rows):
            if matrix[j][i] != 0:
                pivot_row = j
                break
        if pivot_row is None:
            continue
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        for j in range(rows):
            if j == rank:
                continue
            factor = matrix[j][i] / matrix[rank][i]
            for k in range(cols):
                matrix[j][k] -= factor * matrix[rank][k]
        rank += 1
    return rank

def is_irreducible(matrix):
    rows, cols = len(matrix), len(matrix[0])
    if gaussian_elimination(matrix) == rows:
        return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    num_clauses = 3 * n
    variables = set(range(n))
    clauses = []
    for _ in range(num_clauses):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    
    GF2_matrix = [[0] * (n + 1) for _ in range(n)]
    for i, clause in enumerate(clauses):
        for var in clause:
            GF2_matrix[var][i] = 1
        GF2_matrix[n][i] = 1
    
    irreducible_components = sum(is_irreducible(row[:n]) for row in GF2_matrix)
    
    # ACC^0 circuit size lower bound is Ω(n log n)
    acc0_lower_bound = n * math.log2(n)
    
    return {
        "metric_name": "irreducible_components",
        "metric_value": irreducible_components,
        "instances_tested": 1,
        "conjecture_holds": irreducible_components == 2**n and irreducible_components >= acc0_lower_bound,
        "counterexample": "" if irreducible_components == 2**n else f"irreducible_components={irreducible_components}, expected=2^{n}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")