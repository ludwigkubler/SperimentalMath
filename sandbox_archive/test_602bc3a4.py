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
    
    def generate_circuit(depth):
        if depth == 0:
            return []
        else:
            gate = random.choice(['AND', 'OR'])
            inputs = [generate_circuit(random.randint(1, depth-1)) for _ in range(2)]
            return (gate, inputs)
    
    def calculate_quandle_rank(circuit):
        if not circuit:
            return 0
        elif isinstance(circuit[0], tuple):
            gate, inputs = circuit
            rank = max(calculate_quandle_rank(inp) for inp in inputs)
            return rank + 1
        else:
            return 1
    
    def simulate_communication_protocol(circuit):
        if not circuit:
            return 0
        elif isinstance(circuit[0], tuple):
            gate, inputs = circuit
            return sum(simulate_communication_protocol(inp) for inp in inputs)
        else:
            return 1
    
    depths = [5, 10, 15, 20, 30, 40]
    results = []
    
    for depth in depths:
        for _ in range(17):  # Aim for at least 30 instances per seed
            circuit = generate_circuit(depth)
            rank = calculate_quandle_rank(circuit)
            communication_cost = simulate_communication_protocol(circuit)
            results.append((depth, rank, communication_cost))
    
    n_max = max(max(result[0] for result in results), max(result[1] for result in results))
    if n_max < 16:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max too small"
        }
    
    depth_values = [result[0] for result in results]
    rank_values = [result[1] for result in results]
    communication_cost_values = [result[2] for result in results]
    
    def calculate_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))
    
    correlation_coefficient = calculate_correlation(depth_values, rank_values)
    
    if abs(correlation_coefficient) < 0.7:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"Correlation coefficient {correlation_coefficient} < 0.7"
        }
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient < 0.7' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")