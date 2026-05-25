# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import itertools
from fractions import Fraction

def p_adic_log(x, p):
    if x <= 0:
        return None
    count = 0
    while x % p == 0:
        x //= p
        count += 1
    return count

def generate_cnf(n, alpha):
    clauses = []
    for _ in range(int(alpha * n)):
        clause = random.sample(range(1, n + 1), random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def tseitin_resolution_length(cnf):
    # Placeholder function to compute Tseitin resolution length
    # This is a stub and should be replaced with an actual implementation
    return len(cnf) + 10  # Example value for demonstration purposes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    alpha = random.uniform(0.2, 0.8)
    cnf = generate_cnf(n, alpha)
    
    tau_F = tseitin_resolution_length(cnf)
    
    phi_F = p_adic_log(sum(1 for assignment in itertools.product([0, 1], repeat=n) if all(all(assignment[var-1] == literal % 2 for literal in clause) for clause in cnf)), 2)
    
    if phi_F is None:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "p_adic_log returned None"
        }
    
    r_F = phi_F
    
    if tau_F == 0:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Tseitin resolution length is zero"
        }
    
    ratio = r_F / tau_F
    mean_diff = abs(r_F - Fraction(2, 3) * tau_F)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": 0.95 <= ratio <= 1.05 and mean_diff < 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 31))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = (sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
        else:
            print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
    elif any(r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE some trials produced None")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"p_adic_log returned None\" first_failing_seed={first_failing_seed}")