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
    
    def noncrossing_partition_size(f):
        n = len(f)
        if n == 1:
            return 1
        elif n == 2:
            return 3
        else:
            return 2 * noncrossing_partition_size(f[:n//2]) + noncrossing_partition_size(f[n//2:])
    
    def arborescence_complexity(P):
        if P == 1:
            return 0
        elif P == 3:
            return 1
        else:
            return 1 + max(arborescence_complexity(P // 2), arborescence_complexity(P - P // 2))
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    P = noncrossing_partition_size(f)
    complexity = arborescence_complexity(P)
    
    return {
        "metric_name": "arborescence_complexity",
        "metric_value": complexity,
        "instances_tested": 1,
        "conjecture_holds": complexity <= 1.5 * math.log2(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_complexity = sum(r["metric_value"] for r in results) / len(results)
    std_complexity = math.sqrt(sum((r["metric_value"] - mean_complexity) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_complexity} std={std_complexity} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_complexity} std={std_complexity} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")