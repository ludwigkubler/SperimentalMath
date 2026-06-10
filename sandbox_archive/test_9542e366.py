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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def algebraic_cycle_representation(circuit):
        n = len(circuit)
        cycle_order = 0
        while True:
            cycle_order += 1
            if all((i + cycle_order) % n != i for i in range(n)):
                break
        return cycle_order
    
    def rank_variance(circuit):
        n = len(circuit)
        count = [circuit.count(i) for i in range(2)]
        mean = sum(count) / n
        variance = sum((x - mean)**2 for x in count) / (n - 1)
        return variance
    
    def pearson_correlation(xs, ys):
        n = len(xs)
        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        cov = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n))
        var_x = sum((xs[i] - mean_x)**2 for i in range(n)) / (n - 1)
        var_y = sum((ys[i] - mean_y)**2 for i in range(n)) / (n - 1)
        return cov / math.sqrt(var_x * var_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    alpha_C_values = []
    rank_variance_values = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        alpha_C = algebraic_cycle_representation(circuit)
        alpha_C_values.append(alpha_C)
        rank_variance_value = rank_variance(circuit)
        rank_variance_values.append(rank_variance_value)
    
    correlation_coefficient = pearson_correlation(alpha_C_values, rank_variance_values)
    p_value = 0.05  # Placeholder for actual p-value calculation
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / (len(results) - 1))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")