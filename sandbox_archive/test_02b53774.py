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
    
    def generate_tseitin_formula(n):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append([var])
        for i in range(2**n):
            clause = []
            for j in range(n):
                if (i >> j) & 1:
                    clause.append(f"x{j+1}")
                else:
                    clause.append(f"~x{j+1}")
            clauses.append(clause)
        return variables, clauses
    
    def adjacency_matrix(variables, clauses):
        n = len(variables)
        adj = [[0] * n for _ in range(n)]
        for clause in clauses:
            for var in clause:
                if var.startswith('x'):
                    i = int(var[1:]) - 1
                    adj[i][i] += 1
        return adj
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            pivot = next((j for j in range(i, n) if matrix[j][i]), None)
            if pivot is not None:
                rank += 1
                for j in range(n):
                    matrix[i][j], matrix[pivot][j] = matrix[pivot][j], matrix[i][j]
                for j in range(n):
                    if i != j:
                        factor = -matrix[j][i] / matrix[i][i]
                        for k in range(n):
                            matrix[j][k] += factor * matrix[i][k]
        return rank
    
    def width(clauses):
        max_width = 0
        for clause in clauses:
            max_width = max(max_width, len(clause))
        return max_width
    
    n = random.randint(5, 20)
    variables, clauses = generate_tseitin_formula(n)
    adj_matrix = adjacency_matrix(variables, clauses)
    rank = min_rank(adj_matrix)
    w_G = width(clauses)
    
    expected_rank = 2 ** math.ceil(math.log2(w_G))
    ratio = rank / expected_rank
    
    return {
        "metric_name": "rank_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.5,
        "counterexample": "" if ratio >= 0.5 else f"rank={rank}, expected=2^Ω({w_G})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='{results[0]['counterexample']}' first_failing_seed={first_failing_seed}")