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
    n = 20
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    M_d = [[0] * n for _ in range(n)]
    
    # Compute the moment matrix M_d
    for i in range(n):
        for j in range(n):
            if i != j and G[i][j] == 1:
                M_d[i][j] = (i + j) / math.sqrt(2 * n)
                M_d[j][i] = M_d[i][j]
    
    # Compute the rank of M_d
    rank = 0
    for i in range(n):
        if all(M_d[j][i] == 0 for j in range(i)):
            rank += 1
    
    metric_value = rank
    conjecture_holds = rank >= math.sqrt(n)
    counterexample = "" if conjecture_holds else "rank < sqrt(n)"
    
    return {
        "metric_name": "Rank of Moment Matrix",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        random.seed(seed)
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank < sqrt(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")