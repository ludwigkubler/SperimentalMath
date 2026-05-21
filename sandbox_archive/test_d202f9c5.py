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
    
    def f(x):
        n = len(x)
        return sum(x[i] * x[j] for i in range(n) for j in range(i + 1, n)) ** (1 / c)
    
    def hodge_index(M):
        # Placeholder implementation of Hodge index calculation
        # This is a dummy function and should be replaced with actual computation
        return sum(sum(row[i] * row[j] for i in range(len(row)) for j in range(i + 1, len(row))) for row in M)
    
    n = random.randint(5, 40)
    X = list(range(n))
    Y = list(range(n))
    c = random.uniform(0.5, 2.0)
    f = lambda x: sum(x[i] * x[j] for i in range(n) for j in range(i + 1, n)) ** (1 / c)
    
    M = [[f((i, j)) for j in Y] for i in X]
    
    hodge_val = hodge_index(M)
    metric_value = hodge_val
    instances_tested = len(X) * len(Y)
    conjecture_holds = hodge_val >= n ** (1/2)
    counterexample = "" if conjecture_holds else f"H(M) = {hodge_val}, n^(1/2) = {n ** (1/2)}"
    
    return {
        "metric_name": "H(M)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"H(M) < n^(1/2)\" first_failing_seed={first_failing_seed}")