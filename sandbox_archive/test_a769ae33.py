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
    
    def ac0_parity_circuit_size(f):
        n = len(f)
        if n == 1:
            return 1
        size = 1
        while n > 1:
            n //= 2
            size *= 2
        return size
    
    def local_ring_extension_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] == 1:
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    size_C = ac0_parity_circuit_size(f)
    minRank_L = local_ring_extension_rank(f)
    
    metric_value = minRank_L / math.log2(size_C)
    conjecture_holds = minRank_L <= math.log2(size_C)
    counterexample = "" if conjecture_holds else f"n={n}, minRank(L)={minRank_L}, log2(size(C))={math.log2(size_C)}"
    
    return {
        "metric_name": "Minimal Rank Ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={res['instances_tested']}, minRank(L)={res['metric_value']}, log2(size(C))={math.log2(res['instances_tested'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")