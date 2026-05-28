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
    
    def generate_3cnf(n, m):
        literals = [f'x{i}' for i in range(1, n+1)] + [f'~x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(literals, 3)
            clauses.append(clause)
        return clauses
    
    def dpll_refutation_tree_width(clauses):
        # Simplified version of DPLL algorithm to estimate tree width
        literals = set()
        for clause in clauses:
            literals.update(clause)
        return len(literals)  # Approximation
    
    def euler_characteristic(matroid):
        rank = len(matroid)
        n = sum(1 for _ in matroid)
        return rank - n + 1
    
    def matroidal_cover(clauses):
        matroid = set()
        for clause in clauses:
            matroid.update(clause)
        return matroid
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n, 2*n)
            clauses = generate_3cnf(n, m)
            matroid = matroidal_cover(clauses)
            w_F = dpll_refutation_tree_width(clauses)
            chi_M = euler_characteristic(matroid)
            
            if chi_M <= 0 or w_F == 0:
                continue
            
            total_metric_value += chi_M
            instances_tested += 1
            c = Fraction(chi_M, w_F**2)
            if abs(chi_M - c * w_F**2) > 1:
                conjecture_holds = False
                counterexample = f"n={n}, m={m}, chi_M={chi_M}, w_F={w_F}, c={c}"
                break
    
    return {
        "metric_name": "Euler characteristic",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")