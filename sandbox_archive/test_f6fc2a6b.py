# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]

    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_dnf(n, size):
        dnf = []
        for _ in range(size):
            clause = set(random.sample(range(n), random.randint(1, n)))
            dnf.append(clause)
        return dnf
    
    def is_k_clique(dnf, k):
        variables = set()
        for clause in dnf:
            variables.update(clause)
        if len(variables) < k:
            return False
        for subset in itertools.combinations(variables, k):
            if all(len(set(subset).intersection(clause)) > 0 for clause in dnf):
                return True
        return False
    
    n = 40
    size_poly_n = int(n ** 1.5)
    size_exp_n = 2 ** (n // 3)
    
    k_clique_dnf = [
        {0, 1, 2}, {0, 1, 3}, {0, 1, 4}, {0, 1, 5}, {0, 1, 6}, {0, 1, 7}, {0, 1, 8}, {0, 1, 9},
        {2, 3, 4}, {2, 3, 5}, {2, 3, 6}, {2, 3, 7}, {2, 3, 8}, {2, 3, 9}, {2, 4, 5}, {2, 4, 6},
        {2, 4, 7}, {2, 4, 8}, {2, 4, 9}, {2, 5, 6}, {2, 5, 7}, {2, 5, 8}, {2, 5, 9}, {2, 6, 7},
        {2, 6, 8}, {2, 6, 9}, {2, 7, 8}, {2, 7, 9}, {2, 8, 9}, {3, 4, 5}, {3, 4, 6}, {3, 4, 7},
        {3, 4, 8}, {3, 4, 9}, {3, 5, 6}, {3, 5, 7}, {3, 5, 8}, {3, 5, 9}, {3, 6, 7}, {3, 6, 8},
        {3, 6, 9}, {3, 7, 8}, {3, 7, 9}, {3, 8, 9}, {4, 5, 6}, {4, 5, 7}, {4, 5, 8}, {4, 5, 9},
        {4, 6, 7}, {4, 6, 8}, {4, 6, 9}, {4, 7, 8}, {4, 7, 9}, {4, 8, 9}, {5, 6, 7}, {5, 6, 8},
        {5, 6, 9}, {5, 7, 8}, {5, 7, 9}, {5, 8, 9}, {6, 7, 8}, {6, 7, 9}, {6, 8, 9}, {7, 8, 9}
    ]
    
    k_clique_rank = gaussian_elimination([[1 if i in clause else 0 for i in range(n)] for clause in k_clique_dnf])
    random_poly_n_rank = gaussian_elimination([[1 if i in clause else 0 for i in range(n)] for clause in generate_random_dnf(n, size_poly_n)])
    random_exp_n_rank = gaussian_elimination([[1 if i in clause else 0 for i in range(n)] for clause in generate_random_dnf(n, size_exp_n)])
    
    return {
        "metric_name": "row_rank",
        "metric_value": k_clique_rank,
        "instances_tested": 3,
        "conjecture_holds": k_clique_rank >= 0.2 * n and random_poly_n_rank <= 5 * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")