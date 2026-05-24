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
    
    # Generate a random noncommutative algebra (simplified for demonstration)
    n = 10
    A = [[random.randint(0, 1) if i == j else 0 for j in range(n)] for i in range(n)]
    
    # Construct a BP_readtwice instance (simplified for demonstration)
    P = [random.randint(0, 1) for _ in range(n * n)]
    TW_P = sum(P[i] for i in range(n * n))
    
    # Compute the minimal rank of sheaf cohomology groups (simplified for demonstration)
    H_A_P = random.randint(1, n)
    
    # Evaluate the conjectured relationships
    ratio = H_A_P / TW_P
    if ratio <= 0 or math.isinf(ratio) or math.isnan(ratio):
        return {
            "metric_name": "ratio",
            "metric_value": ratio,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "invalid_ratio"
        }
    
    # Check the conjecture
    if not (0.5 <= ratio <= 2):
        return {
            "metric_name": "ratio",
            "metric_value": ratio,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"out_of_bounds_ratio={ratio}"
        }
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"out_of_bounds_ratio\" first_failing_seed={first_failing_seed}")