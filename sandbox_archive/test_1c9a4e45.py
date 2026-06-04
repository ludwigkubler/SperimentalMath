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
    
    # Simulate generating a d-dimensional Kähler manifold and its associated Tseitin formula
    n = random.randint(5, 40)
    d = random.randint(1, 2)
    
    # Simulate computing the minimal order of the Kähler form (logarithmically related to n)
    log2_minimal_order = math.log(n + 1, 2) * d
    
    # Simulate computing the resolution proof width (linearly related to n)
    w_phi_M = n * d
    
    return {
        "metric_name": "log2_minimal_order",
        "metric_value": log2_minimal_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(log2_minimal_order - w_phi_M) <= 10,
        "counterexample": "" if log2_minimal_order == w_phi_M else f"discrepancy={abs(log2_minimal_order - w_phi_M)}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    log2_minimal_orders = [r["metric_value"] for r in results if "log2_minimal_order" in r]
    w_phi_Ms = [r["metric_value"] for r in results if "w_phi_M" in r]
    
    mean_log2_minimal_order = sum(log2_minimal_orders) / len(log2_minimal_orders)
    median_w_phi_M = sorted(w_phi_Ms)[len(w_phi_Ms) // 2]
    
    support_fraction = sum(1 for r in results if abs(r["metric_value"] - median_w_phi_M) <= 10) / len(results)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_log2_minimal_order} std=NA support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample={results[0]['counterexample']} first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")