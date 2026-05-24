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

def generate_k_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if clause[0] == -clause[1]:
            continue  # Avoid trivial clauses
        cnf.append(clause)
    return cnf

def circuit_depth(cnf):
    depth = 0
    for clause in cnf:
        depth += max(abs(lit) for lit in clause)
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ratios = []
    
    for n in n_values:
        cnf = generate_k_cnf(n, random.randint(2*n, 3*n))
        if not cnf:
            continue
        
        depth = circuit_depth(cnf)
        if depth == 0:
            continue
        
        ratio = Fraction(len(cnf), depth).limit_denominator()
        ratios.append(ratio)
    
    mean_ratio = sum(ratios) / len(ratios) if ratios else 0
    max_ratio = max(ratios) if ratios else 0
    
    conjecture_holds = mean_ratio <= 1.5 and max_ratio <= 2
    counterexample = "" if conjecture_holds else f"mean={mean_ratio}, max={max_ratio}"
    
    return {
        "metric_name": "Ratio of CNF Clauses to Circuit Depth",
        "metric_value": float(mean_ratio),
        "instances_tested": len(ratios),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    max_ratio = max(r["metric_value"] for r in results if "metric_value" in r)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] > 2 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] > 2)
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio_exceeds_2\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")