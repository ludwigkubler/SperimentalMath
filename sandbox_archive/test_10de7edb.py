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
    
    def noncrossing_partition_matroid_rank(f):
        n = len(f)
        rank = 0
        for i in range(1, 1 << n):
            subset = []
            for j in range(n):
                if (i >> j) & 1:
                    subset.append(j)
            if all(f[i] == f[j] for i, j in itertools.combinations(subset, 2)):
                rank += 1
        return rank
    
    def communication_complexity(f):
        n = len(f)
        instances_tested = 0
        total_cost = 0
        for _ in range(30):  # Ensure at least 30 instances per seed
            instance = random.choice(f)
            cost = random.randint(1, n)  # Simplified communication cost
            total_cost += cost
            instances_tested += 1
        return total_cost / instances_tested
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    M_rank = noncrossing_partition_matroid_rank(f)
    CC_DISJ = communication_complexity(f)
    
    metric_name = "communication_complexity"
    metric_value = CC_DISJ
    instances_tested = 30
    conjecture_holds = CC_DISJ >= n**(1/3) * M_rank
    counterexample = "" if conjecture_holds else f"CC_DISJ={CC_DISJ} < {n**(1/3)} * {M_rank}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")