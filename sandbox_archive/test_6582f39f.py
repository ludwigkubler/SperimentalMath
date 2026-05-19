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
    n = 20
    p = 0.5
    G = [[random.random() < p for _ in range(n)] for _ in range(n)]
    
    # Construct the moment matrix M_d for d=1 (simplified version)
    M_1 = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j]:
                M_1[i][i] += 1
                M_1[j][j] += 1
                M_1[i][j] -= 2
    
    # Compute the rank of M_1
    rank = 0
    for row in M_1:
        if any(row):
            rank += 1
    
    metric_value = rank
    conjecture_holds = rank >= math.sqrt(n)
    counterexample = "" if conjecture_holds else f"Rank {rank} < sqrt({n})"
    
    return {
        "metric_name": "Moment Matrix Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")