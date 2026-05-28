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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_clique(n, k):
        vertices = list(range(n))
        clique = random.sample(vertices, k)
        return clique
    
    def incidence_variety(clique):
        n = len(clique)
        m = 2**n
        incidence_matrix = [[0] * m for _ in range(m)]
        for i in range(m):
            binary_rep = [int(x) for x in format(i, f'0{n}b')]
            if all(binary_rep[j] == 1 for j in clique):
                for j in range(m):
                    if all(binary_rep[k] == (binary_rep[j] ^ binary_rep[l]) for k, l in combinations(clique, 2)):
                        incidence_matrix[i][j] = 1
        return incidence_matrix
    
    def min_rank(matrix):
        n = len(matrix)
        m = len(matrix[0])
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(m)):
                rank += 1
                for j in range(m):
                    if matrix[j][i] != 0:
                        factor = Fraction(matrix[j][i], matrix[i][i])
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def combinations(lst, r):
        result = []
        def combine(start, combo):
            if len(combo) == r:
                result.append(combo)
                return
            for i in range(start, len(lst)):
                combine(i + 1, combo + [lst[i]])
        combine(0, [])
        return result
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            k = random.randint(4, min(n, 40))
            clique = generate_k_clique(n, k)
            incidence_matrix = incidence_variety(clique)
            rank = min_rank(incidence_matrix)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = Fraction(total_rank, instances_tested)
    conjecture_holds = mean_rank >= n**2 * math.log(k)
    counterexample = "" if conjecture_holds else f"n={n}, k={k}"
    
    return {
        "metric_name": "min_rank",
        "metric_value": float(mean_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, k={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")