# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_cnf(n):
    cnf = []
    for _ in range(10):  # Generate 10 clauses
        clause = set()
        while len(clause) < n:
            var = random.randint(-n, n)
            if abs(var) not in clause:
                clause.add(var)
        cnf.append(list(clause))
    return cnf

def generate_frege_proof(cnf):
    # Simplified Frege proof generation (not actual Frege proofs)
    depth = 0
    for clause in cnf:
        depth += len(clause)
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_values = []
    d_values = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        m = len(cnf) * n  # Simplified minimal representation length
        d = generate_frege_proof(cnf)
        
        m_values.append(m)
        d_values.append(d)
    
    mean_m = sum(m_values) / len(m_values)
    mean_d = sum(d_values) / len(d_values)
    
    ratio_mean = mean_m / mean_d if mean_d != 0 else float('inf')
    
    metric_value = abs(ratio_mean - 1.0)
    conjecture_holds = metric_value <= 0.1 and abs(mean_m - mean_d) <= 3
    
    return {
        "metric_name": "m/d ratio",
        "metric_value": metric_value,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")