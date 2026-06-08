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
        inputs = [random.choice([0, 1]) for _ in range(n)]
        outputs = [random.choice([0, 1]) for _ in range(2**n)]
        return inputs, outputs
    
    def communication_complexity(inputs, outputs):
        n = len(inputs)
        max_comm_cost = 0
        for i in range(2**n):
            comm_cost = sum(inputs[j] != outputs[i][j] for j in range(n))
            if comm_cost > max_comm_cost:
                max_comm_cost = comm_cost
        return max_comm_cost
    
    def adjacency_matrix(inputs, outputs):
        n = len(inputs)
        m = 2**n
        adj_matrix = [[0]*m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                if all(inputs[k] == (i >> k & 1) ^ (j >> k & 1) for k in range(n)):
                    adj_matrix[i][j] = 1
        return adj_matrix
    
    def minimal_geometric_entropy(adj_matrix):
        n = len(adj_matrix)
        degree_sum = sum(sum(row) for row in adj_matrix)
        avg_degree = degree_sum / n
        entropy = -avg_degree * math.log(avg_degree, 2)
        return entropy
    
    def calculate_ratio(mGE, c, n):
        if c == 0:
            return None
        return mGE / (c**2 * math.log(n))
    
    instances_tested = 0
    total_mGE = 0.0
    total_c = 0.0
    ratios = []
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        inputs, outputs = generate_instance(n)
        c = communication_complexity(inputs, outputs)
        adj_matrix = adjacency_matrix(inputs, outputs)
        mGE = minimal_geometric_entropy(adj_matrix)
        
        if mGE is not None and c > 0:
            instances_tested += 1
            total_mGE += mGE
            total_c += c
            ratio = calculate_ratio(mGE, c, n)
            if ratio is not None:
                ratios.append(ratio)
    
    if instances_tested == 0:
        return {
            "metric_name": "mGE / (c^2 * log(n))",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_ratio = sum(ratios) / len(ratios)
    support_fraction = len([r for r in ratios if 0.9 <= r <= 1.1]) / len(ratios)
    
    return {
        "metric_name": "mGE / (c^2 * log(n))",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"Ratio out of bounds: {min(ratios)} to {max(ratios)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no valid instances generated")