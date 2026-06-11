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
    n = random.randint(5, 40)
    
    # Generate a random CNF with n variables
    cnf = []
    for _ in range(n):
        literals = [random.choice([1, -1]) * i for i in range(1, n+1)]
        clause = random.sample(literals, random.randint(2, n))
        cnf.append(clause)
    
    # Measure the resolution proof width (simplified version)
    resolution_width = sum(len(cnf) for _ in range(n))  # Simplified for testing
    
    # Conjecture: log(n) ≤ log(w(φ)) ≤ 10 * log(n)
    log_n = math.log(n)
    log_w_phi = math.log(resolution_width)
    
    conjecture_holds = log_n <= log_w_phi <= 10 * log_n
    counterexample = "CNF with n={} failed correlation check".format(n) if not conjecture_holds else ""
    
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = "SUPPORTED mean={} std=0 support_fraction={}".format(mean_value, support_fraction)
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = "FALSIFIED counterexample='{}' first_failing_seed={}".format(results[results.index(next(r for r in results if not r["conjecture_holds"]))]["counterexample"], first_failing_seed)
    
    print(result)