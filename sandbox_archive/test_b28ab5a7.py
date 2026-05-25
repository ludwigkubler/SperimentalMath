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
from fractions import Fraction
import math

def generate_truth_table(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def transform_truth_table_to_braid_representation(truth_table):
    n = int(math.log2(len(truth_table)))
    braid_rep = []
    for i in range(n):
        for j in range(2**(n-i-1)):
            if truth_table[2*j] != truth_table[2*j+1]:
                braid_rep.append((i, j))
    return braid_rep

def min_order(n):
    truth_table = generate_truth_table(n)
    braid_rep = transform_truth_table_to_braid_representation(truth_table)
    return len(braid_rep)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_order = 0
    instances_tested = 0

    for n in n_values:
        order = min_order(n)
        if order == 0:
            return {
                "metric_name": "min_order",
                "metric_value": order,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        total_order += order
        instances_tested += 1

    mean_order = total_order / len(n_values)
    return {
        "metric_name": "min_order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "conjecture_holds": mean_order >= 10 * math.log2(max(n_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")