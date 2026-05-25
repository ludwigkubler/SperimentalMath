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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot row
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            # Swap rows
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            # Eliminate non-pivot elements
            for j in range(i+1, n):
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def min_rank(matrix):
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        return rank
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        # OR clauses
        for i in range(1, n+1):
            clause = [variables[i-1]]
            for j in range(i+1, n+1):
                clause.append('¬' + variables[j-1])
            clauses.append(clause)
        # AND clauses
        for i in range(n):
            clause = ['¬' + variables[i]]
            for j in range(n):
                if j != i:
                    clause.append(variables[j])
            clauses.append(clause)
        return clauses
    
    def config_space_metric(clauses):
        n = len(clauses)
        points = []
        for i in range(2**n):
            point = [0] * n
            for j in range(n):
                if (i >> j) & 1:
                    point[j] = 1
            points.append(point)
        
        distances = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                dist = sum(abs(points[i][k] - points[j][k]) for k in range(n))
                distances[i][j] = dist
                distances[j][i] = dist
        
        return distances
    
    def generate_random_tseitin(n):
        clauses = tseitin_formula(n)
        random.shuffle(clauses)
        return clauses
    
    n = 40
    if n < 5:
        return {
            "metric_name": "min_rank",
            "metric_value": -1,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "n_too_small"
        }
    
    trials = 30
    total_rank = 0
    
    for _ in range(trials):
        clauses = generate_random_tseitin(n)
        metric = config_space_metric(clauses)
        rank = min_rank(metric)
        total_rank += rank
    
    mean_rank = Fraction(total_rank, trials)
    lower_bound = n**2 * math.log(n)
    
    return {
        "metric_name": "min_rank",
        "metric_value": float(mean_rank),
        "instances_tested": trials,
        "conjecture_holds": mean_rank >= lower_bound,
        "counterexample": "" if mean_rank >= lower_bound else f"mean_rank={float(mean_rank)} < {lower_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    lower_bound = max(n**2 * math.log(n) for n in range(5, 41))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] >= lower_bound for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_rank<{lower_bound}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")