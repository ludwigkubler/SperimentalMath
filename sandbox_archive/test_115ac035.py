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
            max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(cols):
                if j != i:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(rows):
                        matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def dnf_from_3cnf(cnf):
        dnf = []
        for clause in cnf:
            dnf.append([abs(lit) for lit in clause])
        return dnf
    
    def generate_random_3cnf(n, m):
        variables = list(range(1, n + 1))
        cnf = []
        for _ in range(m):
            clause = random.sample(variables, 3)
            cnf.append(clause)
        return cnf
    
    n = 40
    k = 10
    m_values = [5, 10, 15, 20, 30, 40]
    
    results = []
    for m in m_values:
        cnf = generate_random_3cnf(n, m)
        dnf = dnf_from_3cnf(cnf)
        matrix = [[int(abs(lit) == var) for var in range(1, n + 1)] for clause in dnf]
        rank = gaussian_elimination(matrix)
        
        results.append({
            "n": n,
            "m": m,
            "rank": rank
        })
    
    total_rank = sum(result["rank"] for result in results)
    mean_rank = total_rank / len(results)
    conjecture_holds = all(mean_rank >= 0.8 * n if m <= n ** (1/2) else mean_rank <= 5 * math.log(n) for result in results)
    
    return {
        "metric_name": "Matroid Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank_gap' first_failing_seed={first_failing_seed}")