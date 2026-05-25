# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_clique_cnf(k, n):
        if k == 1:
            return [[random.randint(1, n)] for _ in range(n)]
        elif k == n:
            return [list(range(1, n + 1))]
        else:
            edges = set(itertools.combinations(range(1, n + 1), 2))
            while len(edges) > (n * (n - 1)) // 2 - k * (k - 1):
                u, v = random.sample(range(1, n + 1), 2)
                if (u, v) in edges:
                    edges.remove((u, v))
            return [[i for i in range(1, n + 1) if (i, j) not in edges] for j in range(1, n + 1)]
    
    def tropical_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for col in range(n):
            pivot_row = None
            for row in range(m):
                if matrix[row][col] != float('-inf'):
                    if pivot_row is None:
                        pivot_row = row
                    else:
                        ratio = Fraction(matrix[pivot_row][col], matrix[row][col])
                        for j in range(n):
                            matrix[row][j] -= ratio * matrix[pivot_row][j]
            if pivot_row is not None:
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n - 1, 3))
    cnf = generate_k_clique_cnf(k, n)
    
    tropical_matrix = [[float('-inf')] * n for _ in range(n)]
    for clause in cnf:
        for literal in clause:
            if literal > 0:
                tropical_matrix[literal - 1][literal - 1] = max(tropical_matrix[literal - 1][literal - 1], 1)
            else:
                tropical_matrix[-literal - 1][-literal - 1] = max(tropical_matrix[-literal - 1][-literal - 1], 1)
    
    rank = tropical_rank(tropical_matrix)
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= 2 ** k,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [593, 631, 677, 727, 773, 821, 877, 929]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if len(results) == 0:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        mean_rank = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
        elif any(not result["conjecture_holds"] for result in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE no_support")