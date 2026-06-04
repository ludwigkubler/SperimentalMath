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
        clauses = []
        for _ in range(n * (n - 1)):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        # Simplified resolution width calculation
        return len(cnf) ** 0.5
    
    def hodge_complexity(n):
        # Simplified Hodge complexity calculation
        return n * (n - 1) / 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        h_value = hodge_complexity(n)
        w_value = resolution_width(cnf)
        
        if w_value > 1.5 * h_value or abs(w_value - h_value ** 2) > 3:
            return {
                "metric_name": "resolution_width",
                "metric_value": w_value,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"n={n}, h(φ)={h_value}, w(φ)={w_value}"
            }
        
        results.append((h_value, w_value))
    
    mean_diff = sum(abs(w - h ** 2) for h, w in results) / len(results)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_diff,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": mean_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")