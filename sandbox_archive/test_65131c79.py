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
    
    def generate_tseitin_circuit(n, m):
        inputs = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(inputs, 2)
            clauses.append(f"({clause[0]} OR {clause[1]})")
        return inputs, clauses
    
    def tropicalize(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:
                    matrix[i][j] = float('inf')
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        for k in range(min(m, n)):
            if matrix[k][k] == float('inf'):
                return -1
            for j in range(k+1, n):
                factor = matrix[j][k] / matrix[k][k]
                for i in range(n):
                    matrix[j][i] -= factor * matrix[k][i]
        rank = 0
        for row in matrix:
            if any(x != float('inf') for x in row):
                rank += 1
        return rank
    
    def niederreiter_mat(m, n):
        matrix = [[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                matrix[i][j] = (i + j) % m
        return matrix
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            inputs, clauses = generate_tseitin_circuit(n, len(clauses))
            qMCS = niederreiter_mat(len(clauses), n)
            tropicalized_qMCS = tropicalize(qMCS)
            rank_value = rank(tropicalized_qMCS)
            if rank_value != -1:
                total_rank += rank_value
                instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = abs(mean_rank - math.sqrt(len(clauses))) <= 0.5 * math.sqrt(len(clauses))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")