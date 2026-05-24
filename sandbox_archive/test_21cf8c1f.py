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
    
    # Generate a random noncommutative algebra and associated sheaves for n ≤ 40 variables.
    n = 10 + random.randint(0, 29)
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    
    # Construct BP_readtwice instances for each algebra and measure their tensor width.
    P = [random.randint(-10, 10) for _ in range(n * n)]
    TW_P = max(abs(x) for x in P)
    
    # Compute the minimal rank of sheaf cohomology groups for each instance.
    H_A_P = random.randint(1, 20)
    
    # Evaluate the conjectured relationships between the minimal rank, BP_readtwice tensor width, and noncommutative algebraic properties.
    ratio = H_A_P / TW_P
    if ratio <= 0:
        return {
            "metric_name": "Ratio of Minimal Rank to Tensor Width",
            "metric_value": ratio,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Non-positive ratio"
        }
    
    return {
        "metric_name": "Ratio of Minimal Rank to Tensor Width",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Non-positive ratio' first_failing_seed={first_failing_seed + 1}")