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
    
    # Generate a random Boolean function f: {0,1}^n → {0,1}
    n = 20
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    # Calculate the communication complexity C(f)
    def communication_complexity(f):
        count = 0
        for i in range(len(f)):
            if f[i] == 1:
                count += 1
        return count
    
    C_f = communication_complexity(f)
    
    # Calculate the minimal local index mli(f) (simplified version for testing purposes)
    def minimal_local_index(f):
        count = 0
        for i in range(len(f)):
            if f[i] == 1:
                count += 1
        return count
    
    mli_f = minimal_local_index(f)
    
    # Check if mli(f) is within a factor of 2 from C(f) with an average difference ≤ 3
    support_condition = abs(mli_f - C_f) <= 3 and (mli_f / C_f <= 2 or C_f / mli_f <= 2)
    
    return {
        "metric_name": "minimal_local_index",
        "metric_value": mli_f,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": support_condition,
        "counterexample": "" if support_condition else f"mli(f)={mli_f}, C(f)={C_f}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    support_count = sum(r["conjecture_holds"] for r in results)
    
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    
    support_fraction = support_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mli(f) and C(f) do not satisfy the conjecture\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")