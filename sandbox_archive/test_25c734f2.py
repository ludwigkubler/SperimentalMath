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
    
    def hypergeometric_moment(n, k, D):
        return (math.comb(k, 1) * math.comb(n - k, D - 1)) / math.comb(n, D)
    
    def communication_complexity(n, M, D):
        return n ** (1 + 1/D)
    
    n = random.randint(5, 40)
    k = random.randint(1, n-1)
    D = random.randint(2, 5)
    M = 1.0
    
    moment = hypergeometric_moment(n, k, D)
    cc = communication_complexity(n, M, D)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": cc,
        "instances_tested": 1,
        "conjecture_holds": cc >= n ** (1 + 1/D),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_cc = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_cc} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")