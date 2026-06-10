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
    
    def generate_tseitin_formula(d):
        n = 2 ** d - 1
        variables = list(range(n))
        clauses = []
        
        # Generate OR clauses
        for i in range(1, n):
            clause = [random.choice(variables) for _ in range(random.randint(1, d))]
            clauses.append(clause)
        
        # Generate NOT clauses
        for var in variables:
            if random.random() < 0.5:
                clauses.append([-var])
        
        return variables, clauses
    
    def adjacency_matrix(n, clauses):
        A = [[0] * n for _ in range(n)]
        for clause in clauses:
            for lit in clause:
                i = abs(lit) - 1
                if lit > 0:
                    A[i][i] = 1
                else:
                    A[-1][i] = 1
                    A[i][-1] = 1
        return A
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            if A[i][i] == 0:
                for j in range(i + 1, n):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    return None  # Singular matrix
            for j in range(n):
                if i == j:
                    continue
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def minimal_order(A):
        rank = 0
        n = len(A)
        for i in range(n):
            if all(A[i][j] == 0 for j in range(i, n)):
                continue
            rank += 1
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return rank
    
    def resolution_width(clauses):
        queue = clauses[:]
        literals_seen = set()
        
        while queue:
            clause1 = queue.pop(0)
            if not clause1:
                continue
            literal = random.choice(clause1)
            literals_seen.add(literal)
            
            for clause2 in queue:
                if -literal in clause2:
                    new_clause = [l for l in clause2 if l != -literal]
                    if not new_clause:
                        return len(queue) + 1
                    queue.append(new_clause)
        
        return len(queue)
    
    n_max = 0
    total_order = 0
    total_width = 0
    instances_tested = 0
    
    for d in [10, 20, 30, 40]:
        for _ in range(7):  # Aim for at least 30 instances per seed
            variables, clauses = generate_tseitin_formula(d)
            n_max = max(n_max, len(variables))
            A = adjacency_matrix(len(variables), clauses)
            order = minimal_order(A)
            width = resolution_width(clauses)
            
            total_order += order
            total_width += width
            instances_tested += 1
    
    mean_order = Fraction(total_order, instances_tested)
    mean_width = Fraction(total_width, instances_tested)
    
    correlation_coefficient = (instances_tested * mean_order * mean_width - 
                               total_order * total_width) / math.sqrt(
                                   (instances_tested * mean_order**2 - total_order**2) *
                                   (instances_tested * mean_width**2 - total_width**2))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else f"Correlation coefficient: {correlation_coefficient}"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_order)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_deviation} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")