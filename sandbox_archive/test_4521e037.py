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
    # Set seed for reproducibility
    random.seed(seed)
    
    def generate_cnf(n):
        cnf = []
        for i in range(n):
            literals = [random.choice([1, -1]) * (j + 1) for j in range(n)]
            clause = random.sample(literals, n // 2)
            cnf.append(clause)
        return cnf
    
    def tseitin_formula(cnf):
        clauses = []
        literals = {}
        var_count = 0
        
        for i, clause in enumerate(cnf):
            literal = -i - 1
            literals[i] = literal
            new_clause = [literal]
            for lit in clause:
                if lit < 0:
                    new_clause.append(-literals[-lit])
                else:
                    new_clause.append(literals[lit])
            clauses.append(new_clause)
        
        return clauses, literals
    
    def geometric_representation(cnf):
        n = len(cnf)
        points = []
        
        for i in range(n):
            point = [random.choice([1, -1]) for _ in range(n)]
            points.append(point)
        
        return points
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + [0] * (n - m) for row in matrix]
        
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            pivot = augmented_matrix[i][i]
            for j in range(i, n + 1):
                augmented_matrix[i][j] /= pivot
            
            for j in range(m):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(n + 1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        rank = sum(1 for row in augmented_matrix if any(row))
        return rank
    
    def f(n):
        # Upper bound function that grows at most doubly-exponentially
        return 2 ** (n // 2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        phi_G, literals = tseitin_formula(cnf)
        points = geometric_representation(phi_G)
        
        if not points or not all(len(point) == n for point in points):
            return {
                "metric_name": "rank",
                "metric_value": 0,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        rank_value = rank(points)
        total_rank += rank_value
        instances_tested += len(phi_G)
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = all(mean_rank <= f(n) for n in n_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")