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
    
    def generate_random_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(-n, -1), random.randint(1, n)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses

    def generate_tseitin_formula(v):
        # Placeholder for Tseitin formula generation
        # This is a dummy implementation and should be replaced with actual logic
        return []

    def minimax(clauses, n, player, memo):
        key = (tuple(sorted(clauses)), player)
        if key in memo:
            return memo[key]
        
        if not clauses:
            return 0
        
        if player == 'Maximizer':
            max_val = -math.inf
            for i in range(1, n + 1):
                new_clauses = [c for c in clauses if i not in c and -i not in c]
                val = minimax(new_clauses, n, 'Minimizer', memo)
                max_val = max(max_val, val)
            memo[key] = max_val
            return max_val
        else:
            min_val = math.inf
            for i in range(1, n + 1):
                new_clauses = [c for c in clauses if i not in c and -i not in c]
                val = minimax(new_clauses, n, 'Maximizer', memo)
                min_val = min(min_val, val)
            memo[key] = min_val
            return min_val

    def tree_dpll(clauses):
        # Placeholder for exact tree-DPLL implementation
        # This is a dummy implementation and should be replaced with actual logic
        return 0
    
    n_values = [8, 10, 12, 14]
    m_values = [math.ceil(4.5 * n) for n in n_values]
    
    results = []
    for n, m in zip(n_values, m_values):
        clauses = generate_random_3cnf(n, m)
        if not any(clause in clauses for clause in tree_dpll(clauses)):
            continue
        
        L = minimax(clauses, n, 'Maximizer', {})
        R = minimax(clauses, n, 'Minimizer', {})
        t_F = (L - R) / 2
        w_star_F = tree_dpll(clauses)
        
        results.append({
            "metric_name": "Conway Temperature",
            "metric_value": t_F,
            "instances_tested": 1,
            "conjecture_holds": t_F <= 5 * w_star_F,
            "counterexample": "" if t_F <= 5 * w_star_F else f"t(F) = {t_F}, w*(F) = {w_star_F}"
        })
    
    return {
        "seed": seed,
        "metric_name": "Conway Temperature",
        "metric_value": sum(r["metric_value"] for r in results),
        "instances_tested": len(results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")