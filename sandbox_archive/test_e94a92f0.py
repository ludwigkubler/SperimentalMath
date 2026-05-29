# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
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
    
    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rref_matrix = gaussian_elimination([row[:] for row in matrix])
        return sum(1 for row in rref_matrix if any(row[j] != 0 for j in range(cols)))
    
    def generate_cnf(n, alpha):
        m = int(alpha * n * (n - 1) / 2)
        cnf = []
        variables = set(range(1, n + 1))
        for _ in range(m):
            clause = random.sample(variables, 2)
            cnf.append(clause)
        return cnf
    
    def hodge_rank(cnf):
        n = len(cnf)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                count = sum(1 for clause in cnf if {i, j} <= set(clause))
                matrix[i][j] = matrix[j][i] = count
        return rank(matrix)
    
    alpha_values = [0.1, 0.25, 0.5, 0.75]
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        total_rank = 0
        for _ in range(5):
            cnf = generate_cnf(n, alpha)
            hodge_r = hodge_rank(cnf)
            total_rank += hodge_r
        avg_rank = total_rank / 5
        results.append((n, avg_rank))
    
    conjecture_holds = all(avg_rank <= n**2 for n, avg_rank in results)
    counterexample = "" if conjecture_holds else f"alpha={results[0][1]/results[0][0]:.2f}, avg_rank={results[-1][1]:.2f}"
    
    return {
        "metric_name": "average_minimal_rank",
        "metric_value": sum(avg_rank for _, avg_rank in results) / len(results),
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")