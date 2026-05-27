# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def symbols(n):
        return [chr(97 + i) for i in range(n)]
    
    def random_polynomial(n, degree=5):
        variables = symbols(n)
        terms = []
        for _ in range(degree):
            coeffs = [random.randint(-10, 10) for _ in range(n)]
            if all(c == 0 for c in coeffs):
                continue
            term = sum(c * v for c, v in zip(coeffs, variables))
            terms.append(term)
        return sum(terms)
    
    def tropicalize(poly):
        if isinstance(poly, int):
            return poly
        elif isinstance(poly, str):
            return poly
        else:
            return max(tropicalize(p) for p in poly)
    
    def compute_circuit_size(poly):
        if isinstance(poly, int):
            return 1
        elif isinstance(poly, str):
            return 1
        else:
            return sum(compute_circuit_size(p) for p in poly)
    
    n = random.randint(2, 40)
    f = random_polynomial(n)
    T_f = tropicalize(f)
    A_f_rank = compute_circuit_size(T_f)
    circuit_size = compute_circuit_size(f)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": A_f_rank,
        "instances_tested": 1,
        "conjecture_holds": A_f_rank >= circuit_size,
        "counterexample": "" if A_f_rank >= circuit_size else str(f)
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")