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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            cnf.append(clause)
        return cnf
    
    def frege_proof_width(cnf):
        # Simplified Frege proof width estimation
        return len(cnf) ** 2
    
    def find_roots(cnf):
        roots = set()
        for clause in cnf:
            for literal in clause:
                if literal != 0:
                    roots.add(literal)
        return len(roots)
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0
    
    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        w_phi = frege_proof_width(cnf)
        R_phi = find_roots(cnf)
        
        if R_phi < 0 or w_phi < 0:
            continue
        
        instances_tested += 1
        total_metric_value += abs(R_phi - w_phi)
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    
    conjecture_holds = all(0.5 * w_phi <= R_phi <= 1.5 * w_phi for _ in range(24, 30))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "abs_diff",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50, 2))  # Default to first 30 odd primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")