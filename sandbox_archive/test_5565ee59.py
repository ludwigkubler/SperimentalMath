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
    
    def generate_circuit(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            inputs = generate_circuit(n // 2)
            outputs = []
            for i in range(len(inputs)):
                outputs.append(random.choice([inputs[i], inputs[(i + 1) % len(inputs)]]))
            return outputs
    
    def compute_ehrhart_rank(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        else:
            rank = 0
            for i in range(n):
                sub_circuit = circuit[:i] + circuit[i+1:]
                rank += compute_ehrhart_rank(sub_circuit)
            return rank
    
    def depth(circuit):
        if len(circuit) == 1:
            return 1
        else:
            return max(depth(circuit[:len(circuit)//2]), depth(circuit[len(circuit)//2:])) + 1
    
    n_max = 40
    instances_tested = 0
    total_rank = 0
    total_depth = 0
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n)
            rank = compute_ehrhart_rank(circuit)
            depth_val = depth(circuit)
            total_rank += rank
            total_depth += depth_val
            instances_tested += 1
    
    if instances_tested < 24:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_rank = total_rank / instances_tested
    mean_depth = total_depth / instances_tested
    
    correlation_coefficient = (instances_tested * mean_rank * mean_depth - 
                               sum(rank * depth for rank, depth in zip(circuit_ranks, circuit_depths))) / \
                              math.sqrt((instances_tested * sum(rank**2 for rank in circuit_ranks) - 
                                          sum(rank**2 for rank in circuit_ranks)) *
                                        (instances_tested * sum(depth**2 for depth in circuit_depths) - 
                                         sum(depth**2 for depth in circuit_depths)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.9 and all(coeff >= 0.7 for coeff in [correlation_coefficient] * instances_tested),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] == "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")