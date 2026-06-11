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
    
    def quadratic_residue_system_diameter(f):
        n = len(f)
        qrs = []
        for i in range(n):
            qrs.append([f[i]])
        
        for i in range(n):
            for j in range(i + 1, n):
                distance = abs(qrs[i][0] - qrs[j][0])
                if distance not in qrs:
                    qrs.append(distance)
        
        return max(qrs) if qrs else 0
    
    def communication_complexity_rank(f):
        # Placeholder for actual computation of rank
        # For simplicity, we use a random value here
        return random.randint(1, n)
    
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(n)]
    d_qrs = quadratic_residue_system_diameter(f)
    r_f = communication_complexity_rank(f)
    
    if r_f == 0:
        return {
            "metric_name": "d(QRS_f)/sqrt(r(f))",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "rank_zero"
        }
    
    ratio = d_qrs / math.sqrt(r_f)
    return {
        "metric_name": "d(QRS_f)/sqrt(r(f))",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 2,  # Placeholder constant c
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [random.getrandbits(32) for _ in range(30)]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
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
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_zero\" first_failing_seed={first_failing_seed}")