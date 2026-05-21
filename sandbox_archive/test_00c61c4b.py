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
    n_values = [8, 10, 12, 14]
    alpha_values = [3.5, 4.0]
    instances_per_seed = 30
    
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for alpha in alpha_values:
            random.seed(seed * 100 + n * 10 + int(alpha * 10))
            
            # Generate a random 3-CNF with clause density α
            clauses = set()
            while len(clauses) < alpha * (n ** 2):
                clause = tuple(random.sample(range(n), 3))
                if clause not in clauses:
                    clauses.add(clause)
            
            # Compute the truth table of f_F
            truth_table = [0] * (1 << n)
            for i in range(1 << n):
                assignment = [(i >> j) & 1 for j in range(n)]
                for clause in clauses:
                    if all(assignment[var] == lit for var, lit in enumerate(clause)):
                        break
                else:
                    truth_table[i] = 1
            
            # Compute all n influences Inf_i
            influences = [0] * n
            for i in range(n):
                pos_count = sum(truth_table[j ^ (1 << i)] for j in range(1 << n))
                neg_count = sum(truth_table[j] for j in range(1 << n) if j & (1 << i))
                influences[i] = max(pos_count, neg_count) / (1 << (n - 1))
            
            # Find the maximum single-variable influence I_max
            I_max = max(influences)
            
            # Run DPLL-with-unit-propagation
            def dpll(alpha, assignment):
                nonlocal tau_KKL
                if alpha == 0:
                    return 1
                remaining_clauses = [c for c in clauses if any(assignment[var] != lit for var, lit in enumerate(c))]
                if not remaining_clauses:
                    return 1
                max_inf_var = influences.index(max(influences))
                tau_KKL += 1
                return dpll(alpha - 1, assignment[:max_inf_var] + [0] + assignment[max_inf_var+1:]) + dpll(alpha - 1, assignment[:max_inf_var] + [1] + assignment[max_inf_var+1:])
            
            tau_KKL = 0
            dpll(alpha, [0] * n)
            
            # Check the conjecture
            metric_value = (1 - I_max) * (n - 1) + 5 * math.sqrt(n)
            if log2(tau_KKL + 1) > metric_value:
                conjecture_holds = False
                counterexample = f"n={n}, alpha={alpha}, seed={seed}"
            
            total_metric_value += metric_value
            instances_tested += 1
    
    return {
        "metric_name": "log2(tau_KKL + 1)",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def log2(x):
    return math.log2(x) if x > 0 else float('-inf')

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")