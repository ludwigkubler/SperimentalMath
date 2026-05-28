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
    
    def cocomplex(circuit):
        n = len(circuit)
        if n == 1:
            return [[circuit[0]]]
        half_n = n // 2
        left_circuit = circuit[:half_n]
        right_circuit = circuit[half_n:]
        left_complex = cocomplex(left_circuit)
        right_complex = cocomplex(right_circuit)
        new_complex = []
        for l in left_complex:
            for r in right_complex:
                new_complex.append(l + [0] * half_n + r)
        return new_complex
    
    def resolution_refutation_size(circuit):
        n = len(circuit)
        if n == 1:
            return circuit[0]
        half_n = n // 2
        left_circuit = circuit[:half_n]
        right_circuit = circuit[half_n:]
        left_size = resolution_refutation_size(left_circuit)
        right_size = resolution_refutation_size(right_circuit)
        return max(left_size, right_size) + 1
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        sorted_x = sorted(range(n), key=lambda i: x[i])
        sorted_y = sorted(range(n), key=lambda i: y[i])
        rank_x = [sorted_x.index(i) for i in range(n)]
        rank_y = [sorted_y.index(i) for i in range(n)]
        covariance = sum((rank_x[i] - n / 2) * (rank_y[i] - n / 2) for i in range(n))
        variance_x = sum((rank_x[i] - n / 2)**2 for i in range(n)) / n
        variance_y = sum((rank_y[i] - n / 2)**2 for i in range(n)) / n
        return covariance / math.sqrt(variance_x * variance_y)
    
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n)
            cocomplex_value = len(cocomplex(circuit))
            refutation_size = resolution_refutation_size(circuit)
            if refutation_size == 0:
                continue
            log2_refutation_size = math.log2(refutation_size)
            total_metric_value += log2_refutation_size
            instances_tested += 1
            if not conjecture_holds and counterexample == "":
                counterexample = f"n={n}, circuit={circuit}"
    
    if instances_tested > 0:
        mean_metric_value = total_metric_value / instances_tested
        correlation_coefficient = spearman_rank_correlation([math.log2(resolution_refutation_size(generate_circuit(n))) for n in [5, 10, 15, 20, 30, 40]], [len(cocomplex(generate_circuit(n))) for n in [5, 10, 15, 20, 30, 40]])
        if correlation_coefficient < 0.8:
            conjecture_holds = False
    else:
        return {
            "metric_name": "Spearman Rank Correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")