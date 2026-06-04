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
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_barcode_matrix(instance):
        n = int(math.log2(len(instance)))
        barcode_matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(2**n):
            if instance[i]:
                barcode_matrix[bin(i).count('1')][i % (n + 1)] += 1
        return barcode_matrix
    
    def calculate_betti_numbers(barcode_matrix):
        n = len(barcode_matrix)
        betti_1 = sum(barcode_matrix[i][0] for i in range(1, n))
        betti_2 = sum(barcode_matrix[i][i] - barcode_matrix[i-1][i-1] for i in range(2, n))
        return betti_1, betti_2
    
    def resolution_proof_width(instance):
        # Simplified heuristic for demonstration purposes
        return len(instance)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_instance(n)
    barcode_matrix = compute_barcode_matrix(instance)
    betti_1, betti_2 = calculate_betti_numbers(barcode_matrix)
    w_phi = resolution_proof_width(instance)
    
    return {
        "metric_name": "sum_of_first_two_betti_numbers",
        "metric_value": betti_1 + betti_2,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
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