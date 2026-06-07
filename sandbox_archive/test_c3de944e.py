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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def symplectic_geometry_degree(f):
        n = len(f)
        count = 0
        for i in range(1 << (n-1)):
            if f[i] != f[~i]:
                count += 1
        return count
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] == f[j]:
                    continue
                rank += 1
        return rank
    
    instances_tested = 0
    msd_values = []
    cvrank_values = []
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        msd = symplectic_geometry_degree(f)
        cvrank = communication_complexity_rank(f)
        
        if msd is None or cvrank is None:
            continue
        
        instances_tested += 1
        msd_values.append(msd)
        cvrank_values.append(cvrank)
    
    if instances_tested == 0:
        return {
            "metric_name": "msd vs cvrank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_msd = sum(msd_values) / instances_tested
    mean_cvrank = sum(cvrank_values) / instances_tested
    
    correlation_coefficient = sum((msd - mean_msd) * (cvrank - mean_cvrank) for msd, cvrank in zip(msd_values, cvrank_values)) / instances_tested
    
    return {
        "metric_name": "msd vs cvrank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(len(f) for f in msd_values + cvrank_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean(abs(msd - cvrank)) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        mean_metric_value = None
        std_metric_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")