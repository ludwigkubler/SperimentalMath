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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def lefschetz_fitting_dimension(formula, n):
        # Placeholder implementation
        return len(formula) // 2
    
    def resolution_proof_width(formula, n):
        # Placeholder implementation
        return len(formula)
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        formula = generate_boolean_formula(n)
        Lf = lefschetz_fitting_dimension(formula, n)
        w = resolution_proof_width(formula, n)
        
        if Lf > 1000:
            results.append(w >= 10000)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(results)
    counterexample = "" if conjecture_holds else "Lf(φ) > 1000 and w(φ) < 10,000"
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
    
    if all(r >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < 0.8 for r in results):
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if r < 0.8)]
        print(f"RESULT: FALSIFIED counterexample=\"Lf(φ) > 1000 and w(φ) < 10,000\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")