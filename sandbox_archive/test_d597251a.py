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
    n = 40
    p = 1.5
    threshold = 0.1 * math.sqrt(n)
    
    random.seed(seed)
    S = set(range(20))
    T = set(range(20))
    M = [[random.choice([0, 1]) if i in S and j in T else 0 for j in range(n)] for i in range(n)]
    
    # Compute the noncommutative L^p norm
    M_scaled = [[M[i][j] / (n * n) ** (1/p) for j in range(n)] for i in range(n)]
    norm_p = 0.0
    for _ in range(500):
        v = [random.random() for _ in range(n)]
        v_norm = sum(x**p for x in v) ** (1/p)
        u = [M_scaled[i][j] * v[j] for j in range(n)]
        u_norm = sum(x**p for x in u) ** (1/p)
        norm_p += u_norm / v_norm
    
    norm_p /= 500.0
    
    result = {
        "metric_name": "noncommutative_Lp_norm",
        "metric_value": norm_p,
        "instances_tested": 1,
        "conjecture_holds": norm_p >= threshold,
        "counterexample": "" if norm_p >= threshold else f"Matrix M did not meet the norm bound (norm={norm_p}, threshold={threshold})"
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_norm_p = sum(r["metric_value"] for r in results) / len(results)
    std_norm_p = math.sqrt(sum((r["metric_value"] - mean_norm_p) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_norm_p} std={std_norm_p} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Matrix M did not meet the norm bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")