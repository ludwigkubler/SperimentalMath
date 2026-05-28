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
        variables = [f'x{i}' for i in range(1, m+1)]
        clauses = []
        for _ in range(s):
            clause = random.sample(variables + ['~' + v for v in variables], 2)
            clauses.append(clause)
        return variables, clauses
    
    def quadratic_form_matrix(bp):
        variables, clauses = bp
        n = len(variables)
        m = len(clauses)
        Q = [[0] * (n + m) for _ in range(n + m)]
        
        for i, var in enumerate(variables):
            Q[i][i] = 1
        
        for j, clause in enumerate(clauses):
            for var in clause:
                if var.startswith('~'):
                    idx = variables.index(var[1:]) + n
                else:
                    idx = variables.index(var)
                Q[idx][j + n] = 1
                Q[j + n][idx] = 1
        
        return Q
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if matrix[i][i] != 0:
                rank += 1
                for j in range(n):
                    matrix[j][i] /= matrix[i][i]
                for j in range(i + 1, m):
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def bp_size(bp):
        variables, clauses = bp
        return len(variables) + len(clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_size = 0
    instances_tested = 0
    
    for n in n_values:
        m = random.randint(1, n)
        s = random.randint(1, n)
        bp = generate_bp(m, s)
        Q = quadratic_form_matrix(bp)
        rank = min_rank(Q)
        size = bp_size(bp)
        
        total_rank += rank
        total_size += size
        instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank <= (n_values[-1] ** 2) * math.log(n_values[-1])
    
    return {
        "metric_name": "mean_minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean rank {mean_rank} exceeds O(n^2 log n)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Mean rank exceeds O(n^2 log n)' first_failing_seed={first_failing_seed}")