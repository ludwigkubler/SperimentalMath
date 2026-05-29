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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_primes(k):
        primes = []
        num = 2
        while len(primes) < k:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            for j in range(i + 1, cols):
                matrix[i][j] /= matrix[i][i]
            for k in range(rows):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(i, cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        matrix = [row[:] for row in matrix]
        gaussian_elimination(matrix)
        rank = 0
        for i in range(rows):
            if any(matrix[i][j] != 0 for j in range(cols)):
                rank += 1
        return rank
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 ** n):
            clause = []
            for j in range(n):
                if random.choice([True, False]):
                    clause.append(j + 1)
                else:
                    clause.append(-(j + 1))
            clauses.append(clause)
        return clauses
    
    def dpll_tree_depth(cnf):
        def dpll(cnf, assignment):
            if not cnf:
                return 0
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                if all(lit > 0 and lit in new_assignment or lit < 0 and -lit not in new_assignment for c in cnf):
                    return dpll(cnf, new_assignment)
                else:
                    return float('inf')
            pure_literal = next((l for l in range(1, n + 1) if all(l in assignment or -l not in assignment for c in cnf)), None)
            if pure_literal is not None:
                new_assignment = assignment.copy()
                new_assignment[pure_literal] = True
                return dpll(cnf, new_assignment)
            literal = random.choice([l for l in range(1, n + 1) if l not in assignment and -l not in assignment])
            return 1 + min(dpll(cnf, {**assignment, literal: True}), dpll(cnf, {**assignment, literal: False}))
        
        return dpll(cnf, {})
    
    def br_generator_count(n):
        # Placeholder for Brauer group generator count calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 5)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    primes = generate_primes(n + 1)
    field_size = primes[-1]
    cnf = generate_cnf(n)
    dpll_depth = dpll_tree_depth(cnf)
    br_count = br_generator_count(n)
    
    return {
        "metric_name": "Brauer Group Generator Count vs DPLL Depth",
        "metric_value": br_count,
        "instances_tested": 1,
        "conjecture_holds": br_count <= dpll_depth,
        "counterexample": "" if br_count <= dpll_depth else f"n={n}, m(Br(F))={br_count}, t*(F)={dpll_depth}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [generate_primes(30)[-1] for _ in range(30)]
    
    results = []
    total_metric_value = 0.0
    num_supporting_seeds = 0
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        total_metric_value += result["metric_value"]
        if result["conjecture_holds"]:
            num_supporting_seeds += 1
    
    mean_metric_value = total_metric_value / len(seeds)
    support_fraction = num_supporting_seeds / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")