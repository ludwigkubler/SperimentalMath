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
    
    def generate_quandle(n):
        quandle = [[i, j] for i in range(n) for j in range(n)]
        return quandle
    
    def calculate_automorphism_group_order(quandle):
        n = len(quandle)
        order = 1
        for i in range(n):
            for j in range(n):
                if (quandle[i][0], quandle[j][1]) == (i, j):
                    order += 1
        return order
    
    def calculate_communication_complexity_rank_variance(circuit):
        n = len(circuit)
        rank_variance = sum([len(set(row)) for row in circuit])
        return rank_variance / n**2
    
    def generate_circuit(n):
        circuit = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return circuit
    
    instances_tested = 0
    n_max = 0
    total_order_sum = 0
    total_variance_sum = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 30:
            break
        
        for _ in range(5):
            circuit = generate_circuit(n)
            quandle = generate_quandle(n)
            order = calculate_automorphism_group_order(quandle)
            variance = calculate_communication_complexity_rank_variance(circuit)
            
            total_order_sum += math.log2(order)
            total_variance_sum += variance
            instances_tested += 1
            n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_order = total_order_sum / instances_tested
    mean_variance = total_variance_sum / instances_tested
    
    correlation_coefficient = (instances_tested * mean_order * mean_variance - 
                               sum(order * variance for order, variance in zip([math.log2(order) for order in range(1, 2**n_max)], [variance for variance in range(1, n_max+1)]))) / \
                              math.sqrt((instances_tested * sum(math.log2(order)**2 for order in range(1, 2**n_max)) - mean_order**2) *
                                        (instances_tested * sum(variance**2 for variance in range(1, n_max+1)) - mean_variance**2))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) > 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")