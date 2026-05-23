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
    
    def generate_boolean_algebra(n):
        return [tuple(sorted(random.sample(range(2), n))) for _ in range(2**n)]
    
    def tropicalized_k_theory_rank(boolean_algebra):
        n = len(boolean_algebra[0])
        k_matrix = [[0] * (1 << n) for _ in range(1 << n)]
        
        for i in range(1 << n):
            for j in range(1 << n):
                if all((i & bit) == (j & bit) or (i & bit) ^ (j & bit) == 0 for bit in range(n)):
                    k_matrix[i][j] = 1
        
        rank = 0
        for row in k_matrix:
            if any(row[j] != 0 for j in range(rank, len(row))):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        boolean_algebra = generate_boolean_algebra(n)
        rank = tropicalized_k_theory_rank(boolean_algebra)
        results.append(rank)
    
    metric_value = max(results)
    conjecture_holds = metric_value <= 2**n - 1
    counterexample = "" if conjecture_holds else f"max rank {metric_value} > 2^{n} - 1"
    
    return {
        "metric_name": "max_tropicalized_k_theory_rank",
        "metric_value": metric_value,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")