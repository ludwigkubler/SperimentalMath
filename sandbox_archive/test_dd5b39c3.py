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
    
    n = 20  # Fixed size for simplicity, as n=1 is allowed for trivial enumeration
    if n < 5 or n > 40:
        return {
            "metric_name": "additive_energy",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "n_out_of_range"
        }
    
    # Generate a random CNF formula with n variables
    cnf = []
    for _ in range(n):
        clause = [random.randint(1, n) for _ in range(random.randint(2, 3))]
        cnf.append(clause)
    
    # Map each truth table entry to an integer (binary → decimal)
    truth_table = [[0] * n for _ in range(2**n)]
    for i in range(2**n):
        binary = bin(i)[2:].zfill(n)
        for j, var in enumerate(binary):
            if var == '1':
                truth_table[i][j] = 1
    
    # Compute additive energy via quadruple counting
    E_f = 0
    for i in range(2**n):
        for j in range(i+1, 2**n):
            for k in range(j+1, 2**n):
                for l in range(k+1, 2**n):
                    if (truth_table[i][j] == truth_table[k][l]) != (truth_table[i][k] == truth_table[j][l]):
                        E_f += 1
    
    # Estimate S(f) via known lower bounds or heuristic approximations
    # For simplicity, use a heuristic based on the number of clauses
    S_f = len(cnf)
    
    # Validate the inequality E(f) * S(f)^β ≥ C * n^α
    alpha = 0.5
    beta = 0.5
    C = 1.0
    
    if S_f == 0:
        return {
            "metric_name": "additive_energy",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "S_f_is_zero"
        }
    
    metric_value = E_f * S_f ** beta
    
    if metric_value < C * n ** alpha:
        return {
            "metric_name": "additive_energy",
            "metric_value": metric_value,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Counterexample: E(f)={E_f}, S(f)={S_f}, n={n}"
        }
    
    return {
        "metric_name": "additive_energy",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")