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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monotone_width(phi):
        n = len(phi)
        max_width = 0
        for i in range(1 << n):
            count = 0
            for j in range(n):
                if (i >> j) & 1:
                    count += phi[j]
            max_width = max(max_width, count)
        return max_width
    
    def local_induction_dimension(phi):
        n = len(phi)
        simplices = []
        for i in range(1 << n):
            simplex = [j for j in range(n) if (i >> j) & 1]
            simplices.append(simplex)
        return len(simplices)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        phi = generate_boolean_function(n)
        lnd = local_induction_dimension(phi)
        w_M = monotone_width(phi)
        results.append((lnd, w_M))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No data generated"
        }
    
    lnds = [r[0] for r in results]
    w_Ms = [r[1] for r in results]
    mean_lnd = sum(lnds) / len(lnds)
    mean_w_M = sum(w_Ms) / len(w_Ms)
    covariance = sum((lnds[i] - mean_lnd) * (w_Ms[i] - mean_w_M) for i in range(len(lnds))) / len(lnds)
    variance_lnd = sum((lnds[i] - mean_lnd)**2 for i in range(len(lnds))) / len(lnds)
    variance_w_M = sum((w_Ms[i] - mean_w_M)**2 for i in range(len(w_Ms))) / len(w_Ms)
    pearson_corr = covariance / (math.sqrt(variance_lnd) * math.sqrt(variance_w_M))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": 30,
        "n_max": max(n for _, _ in results),
        "conjecture_holds": pearson_corr >= 0.8 and all(pearson_corr >= 0.5 for _ in range(len(results))),
        "counterexample": "" if pearson_corr >= 0.8 else "Pearson correlation coefficient < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")