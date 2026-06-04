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
    
    # Parameters for Tseitin formula generation
    d = 3  # Dimension
    n = 20  # Number of variables
    
    # Generate a random Tseitin formula
    literals = [f'x{i}' for i in range(n)]
    clauses = []
    for i in range(n):
        clauses.append([literals[i]])
    for i in range(1, n):
        x_i = literals[i]
        x_j = literals[random.randint(0, i-1)]
        op = random.choice(['or', 'and'])
        if op == 'or':
            clauses.append([x_i, f'~{x_j}'])
        else:
            clauses.append([f'~{x_i}', x_j])
    for clause in clauses:
        clauses.append([f'~{lit}' for lit in clause] + [random.choice(literals)])
    
    # Compute the resolution proof width
    def resolve(clauses):
        new_clauses = set()
        while True:
            added = False
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    if len(set(clauses[i]) & set(clauses[j])) == 1:
                        new_clause = [lit for lit in clauses[i] if lit not in clauses[j]] + \
                                      [lit for lit in clauses[j] if lit not in clauses[i]]
                        new_clauses.add(tuple(sorted(new_clause)))
                        added = True
            if not added:
                break
            clauses.update(new_clauses)
        return len(max(clauses, key=len))
    
    w_phi = resolve(clauses)
    
    # Compute the minimal p-adic valuation of a generator of its associated algebraic variety
    def p_adic_valuation(n):
        if n == 0:
            return float('inf')
        count = 0
        while n % 2 == 0:
            n //= 2
            count += 1
        return count
    
    min_p_val = float('inf')
    for clause in clauses:
        for lit in clause:
            if lit.startswith('~'):
                var = lit[1:]
            else:
                var = lit
            val = p_adic_valuation(int(var))
            if val < min_p_val:
                min_p_val = val
    
    # Compute the length of the longest linear dependency chain
    def longest_linear_dependency(clauses):
        n = len(clauses)
        dp = [1] * n
        for i in range(n):
            for j in range(i):
                if set(clauses[i]) & set(clauses[j]):
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)
    
    l_phi = longest_linear_dependency(clauses)
    
    # Check the inequality
    k = 0
    while True:
        if math.log(min_p_val * w_phi, 2) == n - l_phi + k / 100:
            break
        k += 1
    
    # Compute the metric value
    metric_value = abs(math.log(min_p_val * w_phi, 2) - (n - l_phi))
    
    return {
        "metric_name": "log(p^k(w(φ)))",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": metric_value <= 0.1 * (n - l_phi),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")