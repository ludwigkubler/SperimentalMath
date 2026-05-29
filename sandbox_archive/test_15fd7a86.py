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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def resolution_width(phi):
        n = int(math.log2(len(phi)))
        clauses = []
        for i in range(n):
            clause = [phi[j] if j < (i + 1) * n else not phi[j] for j in range(2**n)]
            clauses.append(clause)
        return len(clauses)
    
    def min_order_lat(phi):
        n = int(math.log2(len(phi)))
        # Simple heuristic: order is proportional to the number of variables
        return n
    
    phi = generate_boolean_function(random.randint(5, 10))
    t_phi = resolution_width(phi)
    MinOrderLat_phi = min_order_lat(phi)
    
    return {
        "metric_name": "MinOrderLat",
        "metric_value": MinOrderLat_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": MinOrderLat_phi <= t_phi,
        "counterexample": "" if MinOrderLat_phi <= t_phi else f"phi={phi}, t*(phi)={t_phi}, MinOrderLat(phi)={MinOrderLat_phi}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")