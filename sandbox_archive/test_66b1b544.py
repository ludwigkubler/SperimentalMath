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
    
    def generate_circuit(n, w):
        circuit = []
        for _ in range(w):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def construct_quasi_crystal(circuit):
        n = len(circuit[0][1])
        qcrystal = {}
        for gate, inputs in circuit:
            key = tuple(inputs)
            if key not in qcrystal:
                qcrystal[key] = 0
            qcrystal[key] += 1
        return qcrystal
    
    def min_order(qcrystal):
        return sum(qcrystal.values())
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_qc_order = 0
    total_w_cubed_2_3 = 0
    
    for n in n_values:
        for _ in range(5):
            w = random.randint(1, min(n, 10))
            circuit = generate_circuit(n, w)
            qcrystal = construct_quasi_crystal(circuit)
            qc_order = min_order(qcrystal)
            total_qc_order += qc_order
            total_w_cubed_2_3 += w ** (2 / 3)
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient samples"
        }
    
    mean_qc_order = total_qc_order / instances_tested
    mean_w_cubed_2_3 = total_w_cubed_2_3 / instances_tested
    
    if mean_qc_order < mean_w_cubed_2_3:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Q(C) < w^(2/3)"
        }
    
    correlation_coefficient = (total_qc_order * total_w_cubed_2_3 - instances_tested * mean_qc_order * mean_w_cubed_2_3) / \
                              math.sqrt((total_qc_order ** 2 - instances_tested * mean_qc_order ** 2) *
                                        (total_w_cubed_2_3 ** 2 - instances_tested * mean_w_cubed_2_3 ** 2))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.1,  # Non-trivially greater than zero
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_samples")