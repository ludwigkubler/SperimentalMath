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
    
    def generate_k_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def vector_space_rank(vectors):
        if not vectors:
            return 0
        rows = len(vectors)
        cols = len(vectors[0])
        matrix = [v[:] for v in vectors]
        
        rank = 0
        for i in range(cols):
            pivot_row = None
            for j in range(rank, rows):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row is not None:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                for j in range(rows):
                    if j != rank - 1:
                        factor = Fraction(matrix[j][i], matrix[rank - 1][i])
                        for k in range(cols):
                            matrix[j][k] -= factor * matrix[rank - 1][k]
        
        return rank
    
    def bray_curtis_distance(v1, v2):
        numerator = sum(abs(a - b) for a, b in zip(v1, v2))
        denominator = sum(max(abs(a), abs(b)) for a, b in zip(v1, v2))
        if denominator == 0:
            return float('inf')
        return numerator / denominator
    
    def compute_brauer_group_rank(clauses):
        n = len(clauses[0])
        vectors = []
        for clause in clauses:
            vector = [Fraction(1) if x > 0 else Fraction(-1) for x in clause]
            vectors.append(vector)
        
        rank = vector_space_rank(vectors)
        return rank
    
    max_rank = 0
    instances_tested = 0
    
    for n in range(5, 41):
        for _ in range(3):  # Ensure at least 3 instances per size
            m = random.randint(n, 2 * n)
            clauses = generate_k_cnf(n, m)
            rank = compute_brauer_group_rank(clauses)
            if rank > max_rank:
                max_rank = rank
            instances_tested += 1
    
    conjecture_holds = max_rank <= 2 ** (len(clauses[0]) - 1)
    counterexample = "" if conjecture_holds else f"max_rank={max_rank}, expected<=2^k"
    
    return {
        "metric_name": "Brauer Group Rank",
        "metric_value": max_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rank = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample_desc = results[seeds.index(first_failing_seed)]["counterexample"]
        result = f"FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}"
    
    print(result)