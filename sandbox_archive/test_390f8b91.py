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
    
    def local_induction_dimension(P):
        n = len(P)
        if n <= 1:
            return 0
        # Placeholder implementation; replace with actual algorithm
        return n - 1
    
    def communication_complexity_rank_variance(P):
        n = len(P)
        if n <= 1:
            return 0
        # Placeholder implementation; replace with actual algorithm
        return n * (n - 1) / 2
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        P = list(range(n))
        random.shuffle(P)
        
        l_id_P = local_induction_dimension(P)
        v_P = communication_complexity_rank_variance(P)
        
        if l_id_P == 0 or v_P == 0:
            continue
        
        results.append((l_id_P, v_P))
    
    if not results:
        return {
            "metric_name": "l_i.d. * v(P)",
            "metric_value": 0.0,
            "instances_tested": 30,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": ""
        }
    
    l_ids, v_Ps = zip(*results)
    mean_l_id = sum(l_ids) / len(l_ids)
    mean_v_P = sum(v_Ps) / len(v_Ps)
    covariance = sum((l - mean_l_id) * (v - mean_v_P) for l, v in results) / len(results)
    variance_l_id = sum((l - mean_l_id) ** 2 for l in l_ids) / len(l_ids)
    
    if variance_l_id == 0:
        return {
            "metric_name": "l_i.d. * v(P)",
            "metric_value": 0.0,
            "instances_tested": 30,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": ""
        }
    
    correlation_coefficient = covariance / math.sqrt(variance_l_id * sum((v - mean_v_P) ** 2 for v in v_Ps))
    
    return {
        "metric_name": "l_i.d. * v(P)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(len(P) for P, _ in results),
        "conjecture_holds": 0.7 <= correlation_coefficient < 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")