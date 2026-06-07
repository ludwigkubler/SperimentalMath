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
    
    def communication_complexity_rank_variance(f, n):
        # Placeholder implementation for rcv
        return sum(f[i] != f[j] for i in range(len(f)) for j in range(i+1, len(f))) / (len(f) * (len(f) - 1))
    
    def minimal_local_induction_dimension(f, n):
        # Placeholder implementation for mild
        return sum(1 for x in range(2**n) if f[x] != f[(x ^ (x >> 1)) % (2**n)])
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rcv = communication_complexity_rank_variance(f, n)
        mild = minimal_local_induction_dimension(f, n)
        results.append({"n": n, "rcv": rcv, "mild": mild})
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    rcvs = [r["rcv"] for r in results]
    mids = [r["mild"] for r in results]
    
    mean_rcv = sum(rcvs) / len(rcvs)
    mean_mid = sum(mids) / len(mids)
    
    correlation = 0
    for i in range(len(results)):
        correlation += (rcvs[i] - mean_rcv) * (mids[i] - mean_mid)
    correlation /= (len(results) * math.sqrt(sum((x - mean_rcv)**2 for x in rcvs)) * math.sqrt(sum((y - mean_mid)**2 for y in mids)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} n_tested={len(results)}")