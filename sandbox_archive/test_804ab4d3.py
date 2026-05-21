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
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot
        max_row = i
        for r in range(i+1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(i+1, rows):
            factor = matrix[j][i] / pivot
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]

    # Count non-zero rows
    rank = sum(1 for row in matrix if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    k = 3
    
    def generate_random_dnf(n, size):
        dnf = []
        while len(dnf) < size:
            clause = set(random.sample(range(n), random.randint(1, n)))
            if all(len(clause & c) <= 1 for c in dnf):
                dnf.append(clause)
        return dnf
    
    def generate_k_clique_dnf(n, k):
        clique = list(range(k))
        dnf = []
        for subset in itertools.combinations(range(n), k-1):
            if len(set(subset) & set(clique)) == k-1:
                dnf.append(set(subset) | {k})
        return dnf
    
    def convert_to_matrix(dnf, n):
        matrix = [[0] * n for _ in range(len(dnf))]
        for i, clause in enumerate(dnf):
            for var in clause:
                matrix[i][var] = 1
        return matrix
    
    # Generate k-clique DNF instance
    clique_dnf = generate_k_clique_dnf(n, k)
    clique_matrix = convert_to_matrix(clique_dnf, n)
    clique_rank = gaussian_elimination(clique_matrix)
    
    # Generate random DNF instance
    random_dnf = generate_random_dnf(n, 100)  # Adjust size for better statistical signal
    random_matrix = convert_to_matrix(random_dnf, n)
    random_rank = gaussian_elimination(random_matrix)
    
    return {
        "metric_name": "row_rank",
        "metric_value": clique_rank,
        "instances_tested": len(clique_dnf) + len(random_dnf),
        "conjecture_holds": clique_rank >= 0.2 * n and random_rank <= 5 * math.log(n, 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"k-clique instance with rank {r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break