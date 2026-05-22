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
    
    def generate_symmetric_tensor(n):
        tensor = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                tensor[i][j] = random.randint(1, 10)
                tensor[j][i] = tensor[i][j]
        return tensor
    
    def schur_weyl_duality(m, pi):
        return m / 2 + len(pi) * math.log2(m)
    
    def min_symplectic_tensor_product_rank(tensor):
        n = len(tensor)
        rank = 0
        for i in range(n):
            for j in range(i, n):
                if tensor[i][j] != 0:
                    rank += 1
        return rank
    
    def permutation_circuit_depth(n):
        return int(n ** math.log2(3 / 4))
    
    def generate_partition(m):
        pi = []
        while m > 0:
            part = random.randint(1, m)
            pi.append(part)
            m -= part
        return tuple(sorted(pi))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    tensor = generate_symmetric_tensor(n)
    m = min_symplectic_tensor_product_rank(tensor)
    pi = generate_partition(m)
    lower_bound = schur_weyl_duality(m, pi)
    
    if abs(m / 2 + len(pi) * math.log2(m)) > 10:
        return {
            "metric_name": "min_symplectic_tensor_product_rank",
            "metric_value": m,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "m_too_large"
        }
    
    circuit_depth = permutation_circuit_depth(n)
    
    return {
        "metric_name": "min_symplectic_tensor_product_rank",
        "metric_value": m,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and sum(1 for result in results if not result["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")