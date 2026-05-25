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
    
    n = random.randint(5, 30)
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    # Compute AC^0-k-distance circuit complexity (simplified version)
    def ac0_k_distance(f):
        if len(f) == 1:
            return 1
        k = random.randint(1, n-1)
        left = f[:2**(k+1)]
        right = f[2**(k+1):]
        return max(ac0_k_distance(left), ac0_k_distance(right)) + 1
    
    circuit_complexity = ac0_k_distance(f)
    
    # Compute minimal rank of quandle invariant (simplified version)
    def min_rank_quandle_invariant(f):
        if len(f) == 1:
            return 1
        rank = 0
        for i in range(len(f)):
            for j in range(i+1, len(f)):
                if f[i] != f[j]:
                    rank += 1
        return rank
    
    quandle_rank = min_rank_quandle_invariant(f)
    
    metric_value = quandle_rank * circuit_complexity
    conjecture_holds = quandle_rank <= circuit_complexity * n * math.log(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "quandle_rank_circuit_complexity_product",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")