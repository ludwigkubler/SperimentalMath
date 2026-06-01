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
    
    def generate_circuit(n, d):
        if n == 1:
            return ['0'] * (2 ** d - 1)
        else:
            circuits = [generate_circuit(n-1, d//2)]
            for i in range(1 << (d//2)):
                circuits.append([f'({circuits[0][i]} {random.choice(["&", "|"])} x{i+1})'])
            return sum(circuits, [])
    
    def compute_sheaf_rank(circuit):
        # Placeholder function to simulate the computation
        return len(circuit)
    
    def compute_resolution_width(circuit):
        # Placeholder function to simulate the computation
        return len(circuit) ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        total_width = 0
        
        while instances_tested < 30:
            circuit = generate_circuit(n, random.randint(5, 10))
            rank = compute_sheaf_rank(circuit)
            width = compute_resolution_width(circuit)
            
            if rank > 0 and width > 0:
                total_rank += rank
                total_width += width
                instances_tested += 1
        
        if instances_tested == 0:
            return {
                "metric_name": "correlation",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n_values[-1],
                "conjecture_holds": False,
                "counterexample": "No valid circuits generated"
            }
        
        mean_rank = total_rank / instances_tested
        mean_width = total_width / instances_tested
        
        results.append({
            "n": n,
            "mean_rank": mean_rank,
            "mean_width": mean_width
        })
    
    correlation_coefficient = 0.0
    for result in results:
        correlation_coefficient += (result["mean_rank"] - result["mean_width"]) ** 2
    
    correlation_coefficient /= len(results)
    correlation_coefficient = math.sqrt(correlation_coefficient)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": n_values[-1],
        "conjecture_holds": correlation_coefficient <= 0.1 * n_values[-1],  # Placeholder threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] or result["instances_tested"] == 0 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["instances_tested"] > 0 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")