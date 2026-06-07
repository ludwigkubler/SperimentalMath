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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause.reverse()
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        queue = set()
        for clause in cnf:
            queue.add(clause[0])
        
        while True:
            new_queue = set()
            for literal in queue:
                if literal > 0:
                    continue
                neg_literal = -literal
                for clause in cnf:
                    if neg_literal in clause and len(clause) == 2:
                        new_clause = [l for l in clause if l != neg_literal]
                        if new_clause not in new_queue:
                            new_queue.add(new_clause)
            if new_queue == queue:
                break
            queue.update(new_queue)
        
        return max(len(cnf), len(queue))
    
    def theta_min(cnf):
        n = len(cnf[0])
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    row, col = literal - 1, n
                else:
                    row, col = -literal - 1, n
                matrix[row][col] += 1
        
        # Gaussian elimination to find rank
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for i in range(cols):
                pivot_row = None
                for j in range(rank, rows):
                    if matrix[j][i] != 0:
                        pivot_row = j
                        break
                if pivot_row is None:
                    continue
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                for j in range(rank, rows):
                    factor = -matrix[j][i] / matrix[rank-1][i]
                    for k in range(i, cols):
                        matrix[j][k] += factor * matrix[rank-1][k]
            return rank
        
        return gaussian_elimination(matrix)
    
    n_max = 40
    instances_tested = 30
    total_theta_min = 0
    total_width = 0
    
    for _ in range(instances_tested):
        cnf = generate_cnf(random.randint(5, n_max))
        theta_min_value = theta_min(cnf)
        width = resolution_width(cnf)
        
        total_theta_min += theta_min_value
        total_width += width
    
    mean_theta_min = total_theta_min / instances_tested
    mean_width = total_width / instances_tested
    
    correlation_coefficient = (instances_tested * sum(theta_min_value * width for theta_min_value, width in zip([theta_min(cnf) for _ in range(instances_tested)], [resolution_width(generate_cnf(random.randint(5, n_max))) for _ in range(instances_tested)])) - instances_tested * mean_theta_min * mean_width) / math.sqrt((instances_tested * sum(theta_min_value**2 for theta_min_value in [theta_min(cnf) for _ in range(instances_tested)]) - instances_tested * mean_theta_min**2) * (instances_tested * sum(width**2 for width in [resolution_width(generate_cnf(random.randint(5, n_max))) for _ in range(instances_tested)]) - instances_tested * mean_width**2))
    
    conjecture_holds = correlation_coefficient >= 0.95
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")