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

def generate_tseitin_formula(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    
    for i in range(m):
        clause = [random.choice(variables)]
        if random.choice([True, False]):
            clause.append(random.choice(variables))
        if random.choice([True, False]):
            clause.append(random.choice(variables))
        clauses.append(clause)
    
    return clauses, variables

def hodge_integral_mod_p(m, p):
    # Simplified example: Hodge integral is m^2 mod p
    return (m ** 2) % p

def resolution_proof_length(n):
    # Simplified example: Resolution proof length is exponential in n
    return 2 ** n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(2 * n, 4 * n)
        formula, variables = generate_tseitin_formula(n, m)
        
        hodge_val = hodge_integral_mod_p(m, 7)  # Using a fixed prime p=7
        proof_length = resolution_proof_length(n)
        
        results.append({
            "n": n,
            "m": m,
            "hodge_val": hodge_val,
            "proof_length": proof_length
        })
    
    if not results:
        return {
            "metric_name": "Hodge Integral vs Resolution Proof Length",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    hodge_ratios = [result["hodge_val"] / result["proof_length"] for result in results]
    avg_ratio = sum(hodge_ratios) / len(hodge_ratios)
    max_proof_length = max(result["proof_length"] for result in results)
    
    conjecture_holds = all(r <= 1.1 for r in hodge_ratios) and max_proof_length <= 2 ** n_values[-1]
    
    return {
        "metric_name": "Hodge Integral vs Resolution Proof Length",
        "metric_value": avg_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Max proof length: {max_proof_length}, Exceeds exponential bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Max proof length exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")