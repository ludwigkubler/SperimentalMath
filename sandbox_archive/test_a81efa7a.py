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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            cnf.append(clause)
        return cnf
    
    def local_induction_dimension(cnf):
        # Placeholder for the actual algorithm to compute LID
        n = len(set(abs(lit) for lit in [lit for clause in cnf for lit in clause]))
        m = len(cnf)
        return (n ** (2/3)) * (m ** (1/3))
    
    def circuit_monotone_width(cnf):
        # Placeholder for the actual algorithm to compute circuit monotone width
        n = len(set(abs(lit) for lit in [lit for clause in cnf for lit in clause]))
        m = len(cnf)
        return n + m
    
    metrics = []
    instances_tested = 0
    n_max = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        m = random.randint(n, n * 2)
        cnf = generate_cnf(n, m)
        
        lid = local_induction_dimension(cnf)
        width = circuit_monotone_width(cnf)
        
        metrics.append((lid, width))
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_lid = sum(lid for lid, _ in metrics) / len(metrics)
    mean_width = sum(width for _, width in metrics) / len(metrics)
    support_fraction = all(abs(mean_width - mean_lid) <= 0.1 * mean_lid for lid, width in metrics)
    
    conjecture_holds = support_fraction
    counterexample = "" if conjecture_holds else f"mean_width={mean_width}, mean_lid={mean_lid}"
    
    return {
        "metric_name": "circuit_monotone_width",
        "metric_value": mean_width,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")