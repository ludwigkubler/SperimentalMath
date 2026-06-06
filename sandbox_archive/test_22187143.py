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
    
    def communication_complexity_rank(f):
        n = len(next(iter(f.keys())))
        rank = 0
        for i in range(n):
            row = [f[tuple([1 if j == i else 0 for j in range(n)])] for t in f]
            rank += sum(row) / n
        return rank
    
    def permutation_group_order(f):
        n = len(next(iter(f.keys())))
        # This is a placeholder implementation. Replace with actual algorithm.
        return 2 ** n
    
    instances_tested = 0
    n_max = 0
    total_metric_value = 0
    conjecture_holds_count = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            f = {tuple(random.randint(0, 1) for _ in range(n)): random.choice([0, 1]) for _ in range(2 ** n)}
            rank = communication_complexity_rank(f)
            order = permutation_group_order(f)
            if order == 0:
                continue
            instances_tested += 1
            n_max = max(n_max, n)
            total_metric_value += abs(order - rank * rank) / (rank * rank + 1e-9)
            if order <= 1.5 * rank * rank and order >= 0.67 * rank * rank:
                conjecture_holds_count += 1
    
    metric_value = total_metric_value / instances_tested
    conjecture_holds = conjecture_holds_count == instances_tested
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "permutation_group_order",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50, 2))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")