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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(matrix, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        factor = matrix[i][i]
        for j in range(i, n):
            matrix[i][j] /= factor
        b[i] /= factor
        
        for j in range(n):
            if i != j:
                factor = matrix[j][i]
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
                b[j] -= factor * b[i]
    
    return [b[i] for i in range(n)]

def tseitin_formula(q, lines, points):
    n = len(lines) + len(points)
    variables = list(range(1, n + 1))
    clauses = []
    
    def add_clause(clause):
        clauses.append(clause)
    
    for line in lines:
        add_clause([line[0], -line[1]])
        add_clause([-line[0], line[1]])
    
    for point in points:
        add_clause([point[0], -point[1]])
        add_clause([-point[0], point[1]])
    
    for i in range(1, n + 1):
        if i <= len(lines):
            add_clause([i])
        else:
            add_clause([-i])
    
    return clauses

def dpll(clauses, assignment):
    if not clauses:
        return True
    unit_clauses = [c[0] for c in clauses if len(c) == 1]
    pure_symbols = {}
    
    for clause in clauses:
        for literal in clause:
            symbol = abs(literal)
            if symbol not in pure_symbols:
                pure_symbols[symbol] = literal > 0
            elif pure_symbols[symbol] != (literal > 0):
                return False
    
    for literal in unit_clauses + list(pure_symbols.keys()):
        new_assignment = assignment.copy()
        new_assignment[literal] = True if literal > 0 else False
        if dpll([c for c in clauses if not any(l in c for l in (literal, -literal))], new_assignment):
            return True
    
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    q_values = [2, 3, 4]
    results = []
    
    for q in q_values:
        lines = [(i, (i * j) % q) for i in range(q) for j in range(1, q)]
        points = [(i, (i + 1) % q) for i in range(q)]
        
        clauses = tseitin_formula(q, lines, points)
        assignment = {i: False for i in range(1, len(clauses) + 1)}
        
        resolution_size = len(dpll(clauses, assignment))
        results.append(resolution_size)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(abs(size - (q_values[0]**3)) < 1 for size in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_size",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r - (q_values[0]**3)) < 1) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(abs(r - (q_values[0]**3)) > 1 for r in results):
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if abs(r - (q_values[0]**3)) > 1)]
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")