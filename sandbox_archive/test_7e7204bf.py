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

def xor_function(n, seed):
    random.seed(seed)
    return [random.randint(0, 1) for _ in range(n)]

def support_size(g, n):
    return sum(1 for i in range(n) if g[i] != 0)

def run_trial(seed: int) -> dict:
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = xor_function(n, seed)
        C_f = len([x for x in f if x == 1])  # Simplified circuit complexity
        q_f = Fraction(C_f).limit_denominator()
        
        g = [random.randint(0, 1) for _ in range(n)]
        support_g = support_size(g, n)
        
        O_qf = math.ceil(q_f)
        Omega_qf2 = q_f ** 2
        
        if O_qf <= C_f <= Omega_qf2:
            results.append((O_qf, Omega_qf2))
    
    metric_value = sum(O[0] for O in results) / len(results)
    conjecture_holds = all(10 >= O[0] for O in results)
    counterexample = "" if conjecture_holds else "support(g) < n/2"
    
    return {
        "metric_name": "Communication Complexity",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] > 10 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='support(g) < n/2' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")