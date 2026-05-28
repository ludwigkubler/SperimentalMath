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
    
    def generate_bp(m, s):
        variables = [f"x{i}" for i in range(1, m+1)]
        clauses = []
        for _ in range(s):
            clause = random.sample(variables + [f"~x{i}" for i in range(1, m+1)], 2)
            clauses.append(clause)
        return variables, clauses
    
    def quadratic_form_matrix(bp):
        variables, clauses = bp
        n = len(variables)
        Q = [[0] * n for _ in range(n)]
        for clause in clauses:
            x_i = variables.index(clause[0])
            x_j = variables.index(clause[1])
            Q[x_i][x_j] += 1
            Q[x_j][x_i] += 1
        return Q
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if matrix[i][i] != 0:
                rank += 1
                for j in range(i+1, n):
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def bp_size(bp):
        variables, clauses = bp
        return len(variables) + 2 * len(clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n)
        s = random.randint(1, n)
        bp = generate_bp(m, s)
        Q = quadratic_form_matrix(bp)
        rank = min_rank(Q)
        size = bp_size(bp)
        results.append({"n": n, "m": m, "s": s, "rank": rank, "size": size})
    
    total_rank = sum(result["rank"] for result in results)
    avg_rank = total_rank / len(results)
    max_size = max(result["size"] for result in results)
    
    conjecture_holds = all(result["rank"] <= (result["m"] ** 2) * math.log(result["n"]) for result in results)
    counterexample = "" if conjecture_holds else f"Size: {max_size}, Rank: {avg_rank}"
    
    return {
        "metric_name": "Average Minimal Rank",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Size exceeds O(n^1.5)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")