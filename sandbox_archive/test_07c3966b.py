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

def generate_3cnf(n):
    literals = [f'x{i}' for i in range(1, n+1)] + [f'~x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(2*n):
        clause = random.sample(literals, 3)
        if random.choice([True, False]):
            clause[0] = '~' + clause[0]
            clause[1] = '~' + clause[1]
            clause[2] = '~' + clause[2]
        clauses.append(' & '.join(clause))
    return ' | '.join(clauses)

def solve_system(literals, clauses):
    n = len(literals) // 2
    A = [[0 for _ in range(n)] for _ in range(n)]
    b = [0] * n
    
    for clause in clauses:
        literals_in_clause = set()
        for literal in clause.split(' & '):
            if literal.startswith('~'):
                literals_in_clause.add(literal[1:])
            else:
                literals_in_clause.add(literal)
        
        for lit1 in literals_in_clause:
            i = literals.index(lit1) // 2
            A[i][i] += 1
        
        for lit1, lit2 in itertools.combinations(literals_in_clause, 2):
            i = literals.index(lit1) // 2
            j = literals.index(lit2) // 2
            if i != j:
                A[i][j] -= Fraction(1, 2)
                A[j][i] -= Fraction(1, 2)
    
    for i in range(n):
        b[i] = Fraction(1, 2)
    
    # Gaussian elimination with partial pivoting
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    
    # Count distinct real points
    num_real_points = 0
    for i in range(n):
        if abs(x[i]) < 1e-6:
            continue
        num_real_points += 1
    
    return num_real_points

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_3cnf(n)
        literals = list(set(literal.strip('~') for literal in formula.split(' | ')))
        num_real_points = solve_system(literals, formula.split(' | '))
        
        result = {
            "metric_name": "num_real_points",
            "metric_value": num_real_points,
            "instances_tested": 1,
            "conjecture_holds": None,
            "counterexample": ""
        }
        
        if n == 5:
            result["conjecture_holds"] = num_real_points >= 2
        elif n == 10:
            result["conjecture_holds"] = num_real_points >= 4
        elif n == 15:
            result["conjecture_holds"] = num_real_points >= 6
        elif n == 20:
            result["conjecture_holds"] = num_real_points >= 8
        elif n == 30:
            result["conjecture_holds"] = num_real_points >= 10
        elif n == 40:
            result["conjecture_holds"] = num_real_points >= 12
        
        results.append(result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "metric_name": "num_real_points",
        "mean_metric_value": total_metric_value / len(results),
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    # Compute mean/std of metric_value and fraction of seeds where conjecture_holds
    total_metric_values = [result["mean_metric_value"] for result in seeds]
    support_fractions = [result["support_fraction"] for result in seeds]
    
    mean_metric_value = sum(total_metric_values) / len(seeds)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in total_metric_values) / len(seeds))
    support_fraction = sum(support_fractions) / len(seeds)
    
    if all(result["conjecture_holds"] for result in seeds):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in seeds):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")