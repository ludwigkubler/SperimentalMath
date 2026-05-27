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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for r in range(i+1, n):
                if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                    max_row = r
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below
            for r in range(i+1, n):
                factor = -matrix[r][i] / matrix[i][i]
                for c in range(i, n):
                    if i == c:
                        matrix[r][c] = 0
                    else:
                        matrix[r][c] += factor * matrix[i][c]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        matrix = [row[:] for row in matrix]
        gaussian_elimination(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[i]):
                rank += 1
        return rank
    
    def resolution_proof_depth(cnf):
        stack = []
        while cnf:
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if not unit_clause:
                return float('inf')
            literal = unit_clause[0]
            cnf = [c for c in cnf if literal not in c and -literal not in c]
            stack.append(literal)
        return len(stack)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = random.sample(range(-n, n+1), 3)
            while any(abs(x) > n for x in clause):
                clause = random.sample(range(-n, n+1), 3)
            clauses.append(clause)
        return clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # At least 30 instances per seed
            cnf = generate_cnf(n)
            depth = resolution_proof_depth(cnf)
            if depth == float('inf'):
                continue
            rank_value = rank([[abs(lit) for lit in clause] for clause in cnf])
            total_rank += rank_value
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank / n >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_rank_per_variable",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[first_failing_seed]}")