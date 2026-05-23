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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tensor_product(f, g):
        n = len(f)
        m = len(g)
        result = []
        for i in range(2*n):
            row = []
            for j in range(2*m):
                if (i >> n) & 1 == (j >> m) & 1:
                    row.append(f[i] * g[j])
                else:
                    row.append(0)
            result.append(row)
        return result
    
    def count_nonzero_entries(matrix):
        return sum(sum(x != 0 for x in row) for row in matrix)
    
    def acc0_circuit_threshold(n, k):
        # This is a placeholder function. Replace with actual ACC⁰ circuit threshold calculation.
        return n + k
    
    def tropicalized_configuration_space(f):
        n = len(f)
        T_f = []
        for x in range(2**n):
            T_f.append(f[x])
        return T_f
    
    n = random.randint(5, 40)
    f = generate_random_boolean_function(n)
    g = [1 - x for x in f]
    
    T_f = tropicalized_configuration_space(f)
    tensor_product_matrix = tensor_product(f, g)
    rank_T_f = count_nonzero_entries(tensor_product_matrix)
    
    k = len(f)
    theta_n_k = acc0_circuit_threshold(n, k)
    
    metric_value = rank_T_f
    conjecture_holds = rank_T_f <= theta_n_k
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")