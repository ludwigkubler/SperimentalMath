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
            # Find pivot row
            max_row = i
            for r in range(i + 1, rows):
                if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                    max_row = r
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below pivot
            for r in range(i + 1, rows):
                factor = matrix[r][i] / matrix[i][i]
                for c in range(cols):
                    matrix[r][c] -= factor * matrix[i][c]
        
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def generate_random_3cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 3)
            clause.append(random.choice([-1, 1]))
            clauses.append(clause)
        return clauses
    
    def generate_kclique_3cnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(k):
            clique = random.sample(variables, 2)
            for j in range(k):
                if i != j:
                    clause = [clique[0], -clique[1]]
                    clause.append(random.choice([-1, 1]))
                    clauses.append(clause)
        return clauses
    
    n = 30
    m_random = int(0.5 * n * (n - 1))
    m_kclique = int(0.5 * k * (k - 1))
    
    random_clauses = generate_random_3cnf(n, m_random)
    kclique_clauses = generate_kclique_3cnf(n, k)
    
    random_matrix = [[int(abs(clause) == var) for var in range(1, n + 1)] for clause in random_clauses]
    kclique_matrix = [[int(abs(clause) == var) for var in range(1, n + 1)] for clause in kclique_clauses]
    
    random_rank = gaussian_elimination(random_matrix)
    kclique_rank = gaussian_elimination(kclique_matrix)
    
    return {
        "metric_name": "matroid_rank",
        "metric_value": random_rank - kclique_rank,
        "instances_tested": 2,
        "conjecture_holds": random_rank >= n and kclique_rank <= math.log(n, 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")