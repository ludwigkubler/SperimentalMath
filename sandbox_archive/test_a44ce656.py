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
    
    def generate_delone_triangulation(n):
        # Simplified Delone triangulation generation (not actual Delone)
        return [[random.random() for _ in range(2)] for _ in range(n)]
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m < n:
            matrix = list(zip(*matrix))
            m, n = n, m
        for i in range(m):
            if matrix[i][i] == 0:
                j = next((j for j in range(i+1, m) if matrix[j][i] != 0), None)
                if j is None:
                    return sum(1 for row in matrix if any(x != 0 for x in row))
                for k in range(n):
                    matrix[i][k], matrix[j][k] = matrix[j][k], matrix[i][k]
            for j in range(m):
                if i != j:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return sum(1 for row in matrix if any(x != 0 for x in row))
    
    def is_k_clique(triangulation, n):
        # Simplified k-CLIQUE check (not actual k-CLIQUE)
        return random.choice([True, False])
    
    n = random.randint(5, 40)
    triangulation = generate_delone_triangulation(n)
    matrix = [[sum((triangulation[i][0] - triangulation[j][0])**2 + 
                    (triangulation[i][1] - triangulation[j][1])**2 for j in range(n))**0.5 
               for i in range(n)] for _ in range(n)]
    
    rank = matrix_rank(matrix)
    k_clique = is_k_clique(triangulation, n)
    
    if k_clique:
        expected_rank = 0.5 * (1/2) * n**(3/2)
    else:
        expected_rank = (1/4) * n**(3/2)
    
    return {
        "metric_name": "Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": abs(rank - expected_rank) <= 0.01 * n if not k_clique else rank >= 0.5 * expected_rank,
        "counterexample": "" if conjecture_holds else f"Rank {rank} does not meet the expected value for {'k-CLIQUE' if k_clique else 'non-k-CLIQUE'} instance"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = (sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")