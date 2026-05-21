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

def gaussian_elimination(matrix):
    n = len(matrix)
    m = len(matrix[0])
    rank = 0
    
    for i in range(n):
        if rank >= m:
            break
        
        pivot_row = i
        while pivot_row < n and matrix[pivot_row][i] == 0:
            pivot_row += 1
        
        if pivot_row == n:
            continue
        
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        
        for j in range(n):
            if i != j:
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(m):
                    matrix[j][k] += factor * matrix[i][k]
        
        rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    k_clique_dnf = [
        {0, 1, 2}, {0, 3, 4}, {1, 5, 6}, {2, 7, 8}, {3, 9, 10},
        {4, 11, 12}, {5, 13, 14}, {6, 15, 16}, {7, 17, 18}, {8, 19, 20}
    ]
    
    k_clique_rank = gaussian_elimination([[1 if i in clause else 0 for i in range(n)] for clause in k_clique_dnf])
    random_dnf_size = random.randint(5, n * (n - 1) // 2)
    random_dnf = set()
    while len(random_dnf) < random_dnf_size:
        clause = {random.randint(0, n - 1) for _ in range(random.randint(1, n))}
        if clause not in random_dnf and all(len(clause & other_clause) <= 1 for other_clause in random_dnf):
            random_dnf.add(frozenset(clause))
    
    random_dnf_rank = gaussian_elimination([[1 if i in clause else 0 for i in range(n)] for clause in random_dnf])
    
    return {
        "metric_name": "row_rank",
        "metric_value": k_clique_rank,
        "instances_tested": 2,
        "conjecture_holds": k_clique_rank >= 0.2 * n and random_dnf_rank <= 5 * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [3, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='k-clique rank too low' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")