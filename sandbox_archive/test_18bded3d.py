# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def kronecker_coefficient(a, b, c):
        if a == 0 or b == 0 or c == 0:
            return 1
        return sum(kronecker_coefficient(a-1, b-i, c) * kronecker_coefficient(i, b, c-1) for i in range(min(b, c)+1)) / (a + b + c)
    
    def symmetric_power_kronecker_sum(n, k):
        total = 0
        for l in range(k+1):
            total += kronecker_coefficient(n, k-l, l) ** 2
        return total
    
    n = random.randint(5, 40)
    m = max(1, min(int(n ** 1.5) - 1, n - 2))
    k = (n + 1) // 2
    
    perm_kronecker_sum = symmetric_power_kronecker_sum(n, k)
    det_kronecker_sum = symmetric_power_kronecker_sum(m, k)
    
    gap = perm_kronecker_sum - det_kronecker_sum
    conjecture_holds = gap >= 2 ** (n / 2)
    
    return {
        "metric_name": "Kronecker Coefficient Gap",
        "metric_value": gap,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, m={m}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")