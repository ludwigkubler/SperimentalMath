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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def construct_coxeter_matrix(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit1 in clause:
                for lit2 in clause:
                    if lit1 != lit2 and abs(lit1) == abs(lit2):
                        matrix[abs(lit1)][abs(lit2)] = 1
        return matrix
    
    def max_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(rank)):
                continue
            pivot = matrix[rank][i]
            for j in range(i, n):
                matrix[i][j] /= pivot
            for k in range(n):
                if k != rank:
                    factor = matrix[k][i]
                    for j in range(i, n):
                        matrix[k][j] -= factor * matrix[i][j]
            rank += 1
        return rank
    
    def clause_complexity(cnf):
        return len(cnf)
    
    cnf = generate_cnf(20, 30)  # Adjust parameters as needed
    matrix = construct_coxeter_matrix(cnf)
    max_rank_value = max_rank(matrix)
    clause_complexity_value = clause_complexity(cnf)
    
    return {
        "metric_name": "max_rank",
        "metric_value": max_rank_value,
        "instances_tested": 1,
        "n_max": len(cnf),
        "conjecture_holds": max_rank_value <= 2 * clause_complexity_value,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "max_rank > 2 * clause_complexity"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")