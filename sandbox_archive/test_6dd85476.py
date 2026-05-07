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

def generate_random_3cnf(n, density):
    clauses = []
    for _ in range(int(density * n * (n - 1) / 2)):
        literals = [random.choice([i, -i]) for i in range(1, n + 1)]
        random.shuffle(literals)
        clause = literals[:3]
        if len(set(clause)) == 3:
            clauses.append(tuple(sorted(clause)))
    return clauses

def generate_php_m(m):
    variables = list(range(1, m * (m + 1) + 1))
    clauses = []
    for i in range(1, m + 1):
        for j in range(i + 1, m + 1):
            clauses.append((i, -j))
            clauses.append((-i, j))
    return clauses

def generate_tseitin_formula(n):
    variables = list(range(1, n * 3 + 1))
    clauses = []
    for i in range(1, n + 1):
        clauses.append((i, i + n, -i - 2 * n))
        clauses.append((-i, -i - n, i + 2 * n))
    return clauses

def duval_algorithm(b):
    n = len(b) // 2
    factors = []
    i = 0
    while i < len(b):
        j = i + 1
        k = i
        while j < len(b) and b[j] >= b[k]:
            if b[j] == b[k]:
                k += 1
            else:
                k = i
            j += 1
        factors.append((i, j))
        i = j
    return factors

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    families = [
        (generate_random_3cnf, [10, 15, 20, 25, 30], 4.5),
        (generate_php_m, [3, 4, 5, 6, 7]),
        (generate_tseitin_formula, [4, 5, 6, 7, 8])
    ]
    
    results = []
    for family_func, n_values, density in families:
        for n in n_values:
            clauses = family_func(n) if family_func == generate_php_m else family_func(n, density)
            refutations = []
            for _ in range(10):  # Sample 10 refutations per instance
                dpll_tree = {}  # Simulate DPLL tree
                for clause in clauses:
                    dpll_tree[clause] = True
                    refutations.append(clause)
            
            lyndon_widths = []
            widths = []
            for clause in refutations:
                b = [0] * (2 * n)
                for lit in clause:
                    if lit > 0:
                        b[lit - 1] = 1
                    else:
                        b[-lit - 1] = 1
                factors = duval_algorithm(b)
                lyndon_widths.append(len(factors))
                widths.append(max(sum(1 for _ in range(k, j)) for k, j in factors))
            
            results.extend({
                "metric_name": "Lyndon width",
                "metric_value": lw,
                "instances_tested": len(refutations),
                "conjecture_holds": lw >= math.ceil(math.log2(w + 1)),
                "counterexample": "" if lw >= math.ceil(math.log2(w + 1)) else f"Clause {clause} has {lw} Lyndon factors but width {w}"
            } for lw, w in zip(lyndon_widths, widths))
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_value": mean_value,
        "std_value": std_value,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    all_results = []
    for seed in seeds:
        all_results.extend(run_trial(seed)["results"])
    
    mean_value = sum(result["metric_value"] for result in all_results) / len(all_results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in all_results) / len(all_results))
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed in seeds if not run_trial(seed)["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")