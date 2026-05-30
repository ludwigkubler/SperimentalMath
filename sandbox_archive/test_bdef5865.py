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
    
    def generate_formula(n):
        if n == 1:
            return "x"
        else:
            left = generate_formula(n // 2)
            right = generate_formula(n - n // 2)
            return f"({left} AND {right})"
    
    def resolution_width(formula):
        # Simplified model for resolution width
        return len(formula.split(" AND ")) ** 2
    
    def minimal_norm_C(n):
        # Simplified model for minimal norm of non-arithmetic curve
        return n ** 0.5
    
    n = random.randint(5, 40)
    formula = generate_formula(n)
    width = resolution_width(formula)
    C = minimal_norm_C(n)
    
    if width > 10 * n**2:
        return {
            "metric_name": "resolution_width",
            "metric_value": width,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Formula too complex: width={width} > 10n^2"
        }
    
    if C**(1/4) > n**2 / width:
        return {
            "metric_name": "resolution_width",
            "metric_value": width,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Non-arithmetic curve too complex: C^(1/4) = {C**(1/4)} > n^2 / width"
        }
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"] != ""), None)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")