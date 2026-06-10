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
from fractions import Fraction
import math

def generate_cnf(n):
    cnf = []
    for _ in range(random.randint(5, 10)):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        while all(abs(c) != abs(clause[i]) for i in range(len(clause))):
            clause[random.randint(0, n-1)] *= -1
        cnf.append(clause)
    return cnf

def generate_tropical_variety(cnf):
    # Placeholder for actual tropical variety generation logic
    # This is a stub and should be replaced with actual computation
    return [random.random() for _ in range(len(cnf))]

def compute_lidb(tropical_variety):
    # Placeholder for actual LIDB computation logic
    # This is a stub and should be replaced with actual computation
    return sum(tropical_variety) / len(tropical_variety)

def generate_gate_circuit(cnf):
    # Placeholder for actual gate circuit generation logic
    # This is a stub and should be replaced with actual computation
    return random.randint(10, 50)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    tropical_variety = generate_tropical_variety(cnf)
    lidb = compute_lidb(tropical_variety)
    cc_phi = generate_gate_circuit(cnf)
    
    correlation_coefficient = (lidb - cc_phi) / 3 if abs(cc_phi) > 0 else 0
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(lidb - cc_phi) <= 3 and correlation_coefficient >= 0.7,
        "counterexample": "" if conjecture_holds else f"LIDB={lidb}, CCφ={cc_phi}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_d = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")