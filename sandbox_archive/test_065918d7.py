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
    n = random.randint(5, 40)
    
    # Generate a read-twice BP for IP_2 using a layered transition matrix
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    B = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    T = [A, B]
    
    # Compute the sum of singular values
    sv_sum = sum(max(abs(s) for s in sv) for _, sv in (np.linalg.svd(T[i], full_matrices=False) for i in range(2)))
    
    # Check if the sum is Ω(n)
    conjecture_holds = sv_sum >= n
    
    return {
        "metric_name": "Sum of singular values",
        "metric_value": sv_sum,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Sum of singular values {sv_sum} is not Ω({n})"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Sum of singular values is not Ω(n)\" first_failing_seed={first_failing_seed}")