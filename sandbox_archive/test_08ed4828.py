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
    
    def communication_complexity(f):
        n = len(f)
        if n == 1:
            return 0
        f_left = f[:2**(n-1)]
        f_right = f[2**(n-1):]
        if all(f_left == f_right):
            return communication_complexity(f_left) + 1
        else:
            return max(communication_complexity(f_left), communication_complexity(f_right)) + 1
    
    def minimal_tropical_motivic_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] == 1:
                rank += 1
        return rank
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        c_f = communication_complexity(f)
        mtr_f = minimal_tropical_motivic_rank(f)
        results.append((c_f, mtr_f))
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    c_values = [c for c, _ in results]
    mtr_values = [mtr for _, mtr in results]
    
    mean_c = sum(c_values) / len(c_values)
    mean_mtr = sum(mtr_values) / len(mtr_values)
    std_c = math.sqrt(sum((x - mean_c) ** 2 for x in c_values) / len(c_values))
    std_mtr = math.sqrt(sum((x - mean_mtr) ** 2 for x in mtr_values) / len(mtr_values))
    
    correlation_coefficient = sum((c - mean_c) * (mtr - mean_mtr) for c, mtr in results) / (len(results) * std_c * std_mtr)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_c,
        "instances_tested": len(c_values),
        "n_max": max(len(f) for _, f in results),
        "conjecture_holds": correlation_coefficient >= 0.95,
        "counterexample": "" if correlation_coefficient >= 0.95 else "correlation_coefficient < 0.95"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_c = sum(r["metric_value"] for r in results) / len(results)
    std_c = math.sqrt(sum((r["metric_value"] - mean_c) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_c} std={std_c} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] == "correlation_coefficient < 0.95" for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.95\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")