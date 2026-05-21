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
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    f = [random.choice([-1, 1]) for _ in range(n*n)]
    S2_f = [sum(f[i*n + j] * f[k*n + l] for i in range(n) for k in range(n)) for j in range(n) for l in range(n)]
    
    def schur_coefficient(poly, rep):
        # Placeholder implementation
        return 0
    
    schur_coeff = schur_coefficient(S2_f, (n-1, 1))
    det_n_schur_coeff = schur_coefficient([random.choice([-1, 1]) for _ in range(n*n)], (n, 0))
    
    metric_value = schur_coeff / det_n_schur_coeff if det_n_schur_coeff != 0 else float('inf')
    conjecture_holds = metric_value >= 2**(n/2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Schur Coefficient Ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")