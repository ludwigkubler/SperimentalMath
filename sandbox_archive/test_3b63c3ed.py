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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_entanglement_entropy(boolean_function, n):
        # Simplified version of entanglement entropy calculation
        ones = boolean_function.count(1)
        zeros = len(boolean_function) - ones
        p_one = Fraction(ones, len(boolean_function))
        p_zero = Fraction(zeros, len(boolean_function))
        return -p_one * math.log2(p_one) - p_zero * math.log2(p_zero)
    
    def compute_qubits_needed(n):
        # Simplified version of qubits needed calculation
        return n
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        boolean_function = generate_boolean_function(n)
        entanglement_entropy = compute_entanglement_entropy(boolean_function, n)
        qubits_needed = compute_qubits_needed(n)
        results.append((entanglement_entropy, qubits_needed))
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman rank correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max([n for _, n in results]),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    entanglement_entropies = [r[0] for r in results]
    qubits_needed = [r[1] for r in results]
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        rank_x = {x[i]: i + 1 for i in range(n)}
        rank_y = {y[i]: i + 1 for i in range(n)}
        sum_differences_squared = sum((rank_x[x[i]] - rank_y[y[i]]) ** 2 for i in range(n))
        return 1 - (6 * sum_differences_squared) / (n * (n**2 - 1))
    
    correlation_coefficient = spearman_rank_correlation(entanglement_entropies, qubits_needed)
    
    return {
        "metric_name": "Spearman rank correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max([n for _, n in results]),
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,  # Arbitrary threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")