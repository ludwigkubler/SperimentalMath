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
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def finite_projective_plane(q):
    points = [(x, y) for x in range(q) for y in range(q)]
    lines = []
    for a in range(q):
        for b in range(q):
            if a == 0 and b == 0:
                continue
            line = set()
            for x in range(q):
                y = (a * x + b) % q
                line.add((x, y))
            lines.append(line)
    return points, lines

def cnf_formula(points, lines):
    n = len(points)
    clauses = []
    for line in lines:
        clause = [-1 - i for i in range(n) if (i, 0) not in line]
        clauses.append(clause)
    return clauses

def branch_and_bound(cnf):
    def solve(variables, assignment):
        if all(var in assignment for var in variables):
            if all(all(assignment[var] == val for var, val in clause.items()) for clause in cnf):
                return True
            else:
                return False
        var = next((v for v in variables if v not in assignment), None)
        for val in [0, 1]:
            assignment[var] = val
            if solve(variables, assignment):
                return True
            del assignment[var]
        return False

    n = len(cnf[0])
    variables = list(range(1, n + 1))
    assignment = {}
    return solve(variables, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    q_values = [2, 3]  # Only testing small values for simplicity
    results = []
    
    for q in q_values:
        points, lines = finite_projective_plane(q)
        n = len(points)
        clauses = cnf_formula(points, lines)
        
        mcsp_value = branch_and_bound(cnf=clauses)
        
        if not (q**2 / 2 <= mcsp_value <= 2 * q**2):
            return {
                "metric_name": "MCSP Complexity",
                "metric_value": mcsp_value,
                "instances_tested": len(q_values),
                "conjecture_holds": False,
                "counterexample": f"q={q}, MCSP(Φ)={mcsp_value}"
            }
    
    return {
        "metric_name": "MCSP Complexity",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(q_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= q**2 / 2 and r <= 2 * q**2) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] == False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")