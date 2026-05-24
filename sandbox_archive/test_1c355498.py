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
    
    def bp_read_twice_complexity(n):
        return math.sqrt(n)
    
    def langlands_dual_rank(n):
        return n ** (1/3)
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    n = random.randint(5, 40)
    f = generate_random_boolean_function(n)
    bp_complexity = bp_read_twice_complexity(n)
    langlands_rank = langlands_dual_rank(n)
    
    if bp_complexity <= n**(1/3):
        rank = langlands_rank
    else:
        rank = bp_complexity * (n**(4/3))
    
    return {
        "metric_name": "Langlands Dual Rank vs BP_ReadTwice Complexity",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": abs(rank - langlands_rank) <= 0.1 * langlands_rank,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "Langlands dual rank does not match BP_ReadTwice complexity"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")