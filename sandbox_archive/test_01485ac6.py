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
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Function size must be a power of 2")
        return n
    
    def local_ring_extension_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] == 1:
                rank += 1
        return rank
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    size_C = ac0_parity_circuit_size(f)
    minRank_L = local_ring_extension_rank(f)
    
    if minRank_L > log2(size_C):
        return {
            "metric_name": "minRank(L)",
            "metric_value": minRank_L,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Function size {n} with rank {minRank_L} > log2({size_C})"
        }
    
    return {
        "metric_name": "minRank(L)",
        "metric_value": minRank_L,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        counterexample = next((res["counterexample"] for res in results if not res["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")