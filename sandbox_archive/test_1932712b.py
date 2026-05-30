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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_entanglement_entropy(boolean_function, n):
        # Simplified simulation of entanglement entropy
        # This is a placeholder and should be replaced with actual quantum circuit simulation
        return n * math.log(n)
    
    def count_qubits_needed(boolean_function, n):
        # Placeholder for counting qubits needed for polynomial-time quantum circuit
        # This is a placeholder and should be replaced with actual quantum circuit analysis
        return n
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        boolean_function = generate_boolean_function(n)
        entanglement_entropy = calculate_entanglement_entropy(boolean_function, n)
        qubits_needed = count_qubits_needed(boolean_function, n)
        results.append((entanglement_entropy, qubits_needed))
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman rank correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    entanglement_entropies = [r[0] for r in results]
    qubits_needed = [r[1] for r in results]
    
    def spearman_rank_correlation(x, y):
        rank_x = {v: i for i, v in enumerate(sorted(set(x)), 1)}
        rank_y = {v: i for i, v in enumerate(sorted(set(y)), 1)}
        n = len(x)
        sum_diff_squared_ranks = sum((rank_x[x[i]] - rank_y[y[i]]) ** 2 for i in range(n))
        return 1 - (6 * sum_diff_squared_ranks) / (n * (n**2 - 1))
    
    correlation_coefficient = spearman_rank_correlation(entanglement_entropies, qubits_needed)
    
    return {
        "metric_name": "Spearman rank correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,  # Arbitrary threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_evidence\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")