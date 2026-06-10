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
    
    def generate_boolean_circuit(depth):
        if depth == 1:
            return random.choice([0, 1])
        else:
            left = generate_boolean_circuit(depth - 1)
            right = generate_boolean_circuit(depth - 1)
            return random.choice([left and right, left or right, not left, not right])
    
    def calculate_symplectic_rank(circuit):
        # Simplified symplectic rank calculation for demonstration
        if circuit == 0:
            return 1
        elif circuit == 1:
            return 2
        else:
            return 3
    
    depths = [5, 10, 15, 20, 30, 40]
    circuit_ranks = []
    
    for depth in depths:
        for _ in range(5):  # Generate 5 circuits per depth
            circuit = generate_boolean_circuit(depth)
            rank = calculate_symplectic_rank(circuit)
            circuit_ranks.append((depth, rank))
    
    if not circuit_ranks:
        return {
            "metric_name": "Spearman correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No circuits generated"
        }
    
    depths = [x[0] for x in circuit_ranks]
    ranks = [x[1] for x in circuit_ranks]
    
    def calculate_spearman_correlation(x, y):
        n = len(x)
        rank_x = {v: i + 1 for i, v in enumerate(sorted(set(x)))}
        rank_y = {v: i + 1 for i, v in enumerate(sorted(set(y)))}
        
        d_squared_sum = sum((rank_x[x[i]] - rank_y[y[i]]) ** 2 for i in range(n))
        rho_numerator = n * d_squared_sum
        rho_denominator = (n * (n**2 - 1)) / 6
        
        return 1 - (rho_numerator / rho_denominator)
    
    correlation_coefficient = calculate_spearman_correlation(depths, ranks)
    
    return {
        "metric_name": "Spearman correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(circuit_ranks),
        "n_max": max(depths),
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(x["metric_value"] for x in results if x["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value) ** 2 for x in results if x["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman correlation < 0.9\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=No valid data")