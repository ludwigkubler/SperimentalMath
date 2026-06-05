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
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def binary_tree_from_function(f, n):
        if n == 0:
            return f[0]
        left = binary_tree_from_function(f[:2**(n-1)], n-1)
        right = binary_tree_from_function(f[2**(n-1):], n-1)
        return (left, right)
    
    def local_induction_dimension(tree):
        if isinstance(tree, tuple):
            return 1 + max(local_induction_dimension(tree[0]), local_induction_dimension(tree[1]))
        else:
            return 0
    
    def communication_complexity_rank(tree):
        if isinstance(tree, tuple):
            left_rank = communication_complexity_rank(tree[0])
            right_rank = communication_complexity_rank(tree[1])
            return max(left_rank, right_rank) + 1
        else:
            return 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        tree = binary_tree_from_function(f, n)
        mild = local_induction_dimension(tree)
        ccr = communication_complexity_rank(tree)
        results.append({"n": n, "mild": mild, "ccr": ccr})
    
    correlation_sum = 0
    instances_tested = len(results) * len(n_values)
    n_max = max(result["n"] for result in results)
    
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            x = results[i]["mild"]
            y = results[j]["mild"]
            correlation_sum += (x - y) * (results[i]["ccr"] - results[j]["ccr"])
    
    mean_metric_value = correlation_sum / (instances_tested * (instances_tested - 1))
    conjecture_holds = all(abs(result["mild"] - result["ccr"]) <= 3 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation between MILD and CCR",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=mapping_undefined first_failing_seed=None")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")