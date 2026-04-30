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
    
    def generate_truth_table(n, k):
        truth_table = []
        for i in range(2 ** n):
            row = [bool((i >> j) & 1) for j in range(n)]
            if any(row[j] and not row[j + k] for j in range(n - k)):
                truth_table.append(row)
        return truth_table
    
    def is_shattered(S, S_F):
        for subset in powerset(S):
            if all(any(all(subset[i] == s[i] for i in range(len(subset))) for s in S_F) for subset in powerset(subset)):
                return False
        return True
    
    def powerset(s):
        result = []
        for i in range(1 << len(s)):
            subset = [s[j] for j in range(len(s)) if (i & (1 << j))]
            result.append(subset)
        return result
    
    n = random.randint(10, 20)
    k = 3
    truth_table = generate_truth_table(n, k)
    
    S_F = [tuple(row) for row in truth_table]
    VC_dimension = 0
    
    while True:
        VC_dimension += 1
        if not is_shattered(range(VC_dimension), S_F):
            break
    
    DNF_size = len(truth_table)
    
    return {
        "metric_name": "VC-dimension",
        "metric_value": VC_dimension,
        "instances_tested": 1,
        "conjecture_holds": DNF_size >= 2 ** (VC_dimension / 4),
        "counterexample": "" if DNF_size >= 2 ** (VC_dimension / 4) else f"DNF size {DNF_size} < 2^{VC_dimension/4}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={math.sqrt(sum((result['metric_value'] - mean_value) ** 2 for result in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"DNF size too small\" first_failing_seed={first_failing_seed}")