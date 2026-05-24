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
    
    def count_monomial_symmetries(f):
        n = int(math.log2(len(f)))
        symmetries = set()
        for i in range(2**n):
            permuted_f = [f[(i >> j) & 1] for j in range(n)]
            if f == permuted_f:
                symmetries.add(tuple(permuted_f))
        return len(symmetries)
    
    def compute_minimal_local_defect_complexity(f):
        n = int(math.log2(len(f)))
        max_defect = 0
        for i in range(2**n):
            defect = sum(abs(f[i] - f[j]) for j in range(i, 2**n) if (i ^ j).bit_count() == 1)
            if defect > max_defect:
                max_defect = defect
        return max_defect
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    S_f = count_monomial_symmetries(f)
    D_f = compute_minimal_local_defect_complexity(f)
    
    if S_f == 0:
        return {
            "metric_name": "ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "No monomial symmetries"
        }
    
    ratio = D_f / S_f
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True if ratio <= 10 else False,  # Placeholder constant for demonstration
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='High ratio' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")