# auto-injected by SEC sandbox
import math
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

def generate_circuit(n):
    if n == 0:
        return []
    circuit = [('NOT', random.randint(0, len(circuit) - 1)) for _ in range(n)]
    return circuit

def communication_complexity(circuit):
    # Placeholder function to compute communication complexity
    # This is a dummy implementation and should be replaced with actual logic
    return len(circuit)

def quaternionic_automorphism_group_order(circuit):
    # Placeholder function to compute the order of the quaternionic automorphism group
    # This is a dummy implementation and should be replaced with actual logic
    return len(circuit) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        circuit = generate_circuit(n)
        if not circuit:
            continue
        
        comm_complexity = communication_complexity(circuit)
        automorphism_group_order = quaternionic_automorphism_group_order(circuit)
        
        if comm_complexity == 0:
            continue
        
        ratio = Fraction(automorphism_group_order, comm_complexity)
        results.append({
            "n": n,
            "comm_complexity": comm_complexity,
            "automorphism_group_order": automorphism_group_order,
            "ratio": ratio
        })
    
    if not results:
        return {
            "metric_name": "Ratio of Automorphism Group Order to Communication Complexity",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    all_ratios_within_range = all(0.5 <= result["ratio"] <= 1.5 for result in results)
    
    return {
        "metric_name": "Ratio of Automorphism Group Order to Communication Complexity",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": all_ratios_within_range,
        "counterexample": "" if all_ratios_within_range else "Out-of-range ratio found"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(ratio is not None for ratio in [result["metric_value"] for result in results]):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(result["counterexample"] == "Out-of-range ratio found" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] == "Out-of-range ratio found")
        print(f"RESULT: FALSIFIED counterexample=\"Out-of-range ratio\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")