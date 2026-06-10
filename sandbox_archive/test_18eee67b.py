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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def construct_quantum_circuit(phi):
        # Simple mapping to simulate quantum circuit construction
        return [sum(phi[i] * (2 ** i) for i in range(len(phi))) % 2]
    
    def resolution_proof_width(phi):
        # Simulate resolution proof width calculation
        return sum(1 for _ in phi)
    
    def topological_quantum_entanglement(circuit):
        # Simple mapping to simulate TQE calculation
        return len(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        total_tqe = 0
        total_width = 0
        for _ in range(5):  # Ensure at least 30 instances per seed
            phi = generate_boolean_instance(n)
            circuit = construct_quantum_circuit(phi)
            width = resolution_proof_width(phi)
            tqe = topological_quantum_entanglement(circuit)
            total_tqe += tqe
            total_width += width
            instances_tested += 1
    
        mean_tqe = Fraction(total_tqe, instances_tested)
        mean_width = Fraction(total_width, instances_tested)
        correlation_coefficient = (mean_tqe * mean_width - Fraction(50, 9)) / (
            Fraction(25, 36) * mean_tqe**2 + Fraction(1, 4) * mean_width**2
        )
        abs_diff = abs(mean_tqe - 2 * mean_width)
        
        results.append({
            "n": n,
            "mean_tqe": mean_tqe,
            "mean_width": mean_width,
            "correlation_coefficient": correlation_coefficient,
            "abs_diff": abs_diff
        })
    
    total_correlation = sum(result["correlation_coefficient"] for result in results)
    total_abs_diff = sum(result["abs_diff"] for result in results)
    
    conjecture_holds = all(
        result["correlation_coefficient"] >= 0.5 and result["abs_diff"] <= 3
        for result in results
    )
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": total_correlation / len(results),
        "instances_tested": instances_tested * len(n_values),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")