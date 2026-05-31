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

def generate_boolean_function(n, m):
    return [[random.randint(0, 1) for _ in range(m)] for _ in range(2**n)]

def communication_complexity(f):
    n = int(math.log2(len(f)))
    m = len(f[0])
    comm = 0
    for i in range(2**n):
        for j in range(m):
            if f[i][j] != f[(i ^ (1 << random.randint(0, n-1))) % (2**n)][j]:
                comm += 1
    return comm

def minimal_local_zeta_function_size(f):
    # Placeholder implementation; actual computation depends on the function's properties
    return len(f)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n, n * (n + 1) // 2)
        c = communication_complexity(f)
        mzeta = minimal_local_zeta_function_size(f)
        results.append((c, mzeta))
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_c = sum(c for c, _ in results) / len(results)
    mean_mzeta = sum(mzeta for _, mzeta in results) / len(results)
    std_c = math.sqrt(sum((c - mean_c)**2 for c, _ in results) / len(results))
    std_mzeta = math.sqrt(sum((mzeta - mean_mzeta)**2 for _, mzeta in results) / len(results))
    
    max_deviation = max(abs(c - mzeta) for c, mzeta in results)
    support_fraction = sum(1 for c, mzeta in results if abs(c - mzeta) <= 2) / len(results)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_c,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8 and max_deviation <= 2,
        "counterexample": "" if support_fraction >= 0.8 else f"max_deviation={max_deviation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_c = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_c = math.sqrt(sum((r["metric_value"] - mean_c)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_c} std={std_c} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if result['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")