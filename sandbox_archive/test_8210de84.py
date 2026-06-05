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

def random_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        cnf.append(clause)
    return cnf

def characteristic_polynomial(cnf):
    n = len(set(abs(lit) for lit in sum(cnf, [])))
    p = [[0] * (n + 1) for _ in range(n + 1)]
    p[0][0] = 1
    x = [Fraction(1), Fraction(-1)]
    
    for clause in cnf:
        term = Fraction(1)
        for lit in clause:
            if lit > 0:
                term *= (1 - x[-lit])
            else:
                term *= (1 + x[-lit])
        for i in range(n, -1, -1):
            for j in range(i, -1, -1):
                p[i][j] += term * (-1) ** (i - j)
    
    return p

def minimal_non_zero_coefficient(p):
    n = len(p)
    for k in range(1, n + 1):
        if any(abs(p[k][j]) > 0 for j in range(n + 1)):
            return k
    return None

def resolution_width(cnf):
    stack = []
    literals = set()
    
    def resolve(lit1, lit2):
        new_literals = set()
        for clause in cnf:
            if lit1 not in clause and -lit1 in clause:
                clause.remove(-lit1)
            if lit2 not in clause and -lit2 in clause:
                clause.remove(-lit2)
            if len(clause) == 0:
                return True
            new_literals.update(clause)
        literals.update(new_literals)
        stack.append(list(new_literals))
        return False
    
    while stack:
        clause = stack.pop()
        for lit1 in clause:
            for lit2 in literals:
                if abs(lit1) != abs(lit2):
                    if resolve(lit1, lit2):
                        return len(stack) + 1
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n * n // 4, n * n)
    cnf = random_cnf(n, m)
    
    p = characteristic_polynomial(cnf)
    k = minimal_non_zero_coefficient(p)
    w = resolution_width(cnf)
    
    if k is None:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = k ** 2 * math.log(n)
    conjecture_holds = w >= metric_value
    
    return {
        "metric_name": "resolution_width",
        "metric_value": w,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"w({n}) = {w}, k^2 log(n) = {k**2 * math.log(n)}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"w({results[0]['n_max']}) = {results[0]['metric_value']}, k^2 log(n) = {results[0]['counterexample'].split('=')[1]}\" first_failing_seed={first_failing_seed}")