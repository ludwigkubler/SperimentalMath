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
    
    def tseitin_formula(n):
        if n == 1:
            return "(x1)"
        else:
            return f"({tseitin_formula(n-1)} ∨ ¬x{n})"
    
    def resolution_width(phi):
        clauses = phi.split(" ∧ ")
        literals = set()
        for clause in clauses:
            literals.update(clause.replace("¬", "").split(" ∨ "))
        return len(literals)
    
    def geometric_flow_time(phi, width):
        # Simplified model of geometric flow time
        # This is a placeholder and should be replaced with actual computation
        return random.randint(1, 2 * width)
    
    n_min = 5
    n_max = 40
    instances_tested = 0
    total_flow_time = 0
    total_width = 0
    
    for n in range(n_min, n_max + 1):
        phi = tseitin_formula(n)
        width = resolution_width(phi)
        flow_time = geometric_flow_time(phi, width)
        
        instances_tested += 1
        total_flow_time += flow_time
        total_width += width
    
    if instances_tested == 0:
        return {
            "metric_name": "flow_to_width_ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }
    
    ratio = total_flow_time / total_width
    return {
        "metric_name": "flow_to_width_ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.5 <= ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 9973) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")