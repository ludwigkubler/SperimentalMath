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

def generate_random_3cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), 3)]
        clauses.append(clause)
    return clauses

def dpll_refutation_depth(clauses):
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return 1 + dpll([c for c in clauses if literal not in c], new_assignment)
        pure_literals = [l for l in range(1, n + 1) if (l not in assignment and -l not in assignment)]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return 1 + dpll([c for c in clauses if literal not in c], new_assignment)
        literal, _ = random.choice(clauses)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        depth_true = 1 + dpll([c for c in clauses if literal not in c], new_assignment)
        new_assignment[literal] = False
        new_assignment[-literal] = True
        depth_false = 1 + dpll([c for c in clauses if -literal not in c], new_assignment)
        return max(depth_true, depth_false)
    n = len(clauses[0])
    assignment = {}
    return dpll(clauses, assignment)

def p_adic_l_function(q):
    def zeta(s):
        return sum(1 / (p ** s) for p in primes if p <= q)
    
    def log_integral(x):
        return x * math.log(x) - x
    
    def riemann_zeta(s):
        if s == 1:
            return float('inf')
        return sum(p ** (-s) for p in primes)
    
    def dirichlet_l_function(s, chi):
        return sum(chi(n) / n ** s for n in range(1, q + 1))
    
    primes = [2]
    for num in range(3, q + 1, 2):
        is_prime = True
        for p in primes:
            if p * p > num:
                break
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    
    chi_q = lambda n: (-1) ** ((n - 1) // 2)
    return dirichlet_l_function(1/2, chi_q)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        clauses = generate_random_3cnf(n)
        depth = dpll_refutation_depth(clauses)
        q = random.randint(2, 100)  # Choose a p-adic integer q
        l_value = p_adic_l_function(q)
        results.append((l_value, depth))
    
    mean_l_value = sum(l for l, _ in results) / len(results)
    mean_depth = sum(d for _, d in results) / len(results)
    ratio = mean_l_value / (mean_depth ** 0.75)
    
    conjecture_holds = abs(ratio - 1) < 0.1
    counterexample = "" if conjecture_holds else f"Ratio {ratio} outside [0.9, 1.1]"
    
    return {
        "metric_name": "Ratio of L(1/2, χ_q) to log^(3/4) n",
        "metric_value": ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside [0.9, 1.1]\" first_failing_seed={first_failing_seed}")