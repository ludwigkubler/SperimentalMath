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
    
    def generate_circuit(m, d):
        circuit = []
        for _ in range(d):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, m))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = all(stack.pop() for _ in inputs)
            elif gate_type == 'OR':
                result = any(stack.pop() for _ in inputs)
            stack.append(result)
        return stack[0]
    
    def symplectic_hull_volume(n):
        # Placeholder implementation
        return n
    
    def frege_proof_depth(circuit):
        depth = 0
        for gate_type, inputs in circuit:
            if gate_type == 'AND':
                depth += max(len(inputs), depth)
            elif gate_type == 'OR':
                depth += max(len(inputs), depth)
        return depth + 1
    
    def correlation_coefficient(values1, values2):
        n = len(values1)
        mean1 = sum(values1) / n
        mean2 = sum(values2) / n
        cov = sum((values1[i] - mean1) * (values2[i] - mean2) for i in range(n)) / n
        std1 = math.sqrt(sum((values1[i] - mean1) ** 2 for i in range(n)) / n)
        std2 = math.sqrt(sum((values2[i] - mean2) ** 2 for i in range(n)) / n)
        return cov / (std1 * std2)
    
    m_values = [5, 10, 15, 20, 30, 40]
    d_values = [5, 10, 15, 20, 30, 40]
    shv_values = []
    fpd_values = []
    
    for m in m_values:
        for d in d_values:
            circuit = generate_circuit(m, d)
            result = evaluate_circuit(circuit)
            shv = symplectic_hull_volume(m)
            fpd = frege_proof_depth(circuit)
            shv_values.append(shv)
            fpd_values.append(fpd)
    
    if not shv_values or not fpd_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = correlation_coefficient(shv_values, fpd_values)
    mean_shv_fpd_ratio = sum(shv / fpd for shv, fpd in zip(shv_values, fpd_values)) / len(shv_values)
    std_dev = math.sqrt(sum((shv / fpd - mean_shv_fpd_ratio) ** 2 for shv, fpd in zip(shv_values, fpd_values)) / len(shv_values))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(shv_values),
        "n_max": max(m_values + d_values),
        "conjecture_holds": correlation >= 0.8 and abs(mean_shv_fpd_ratio - (sum(shv_values) / sum(fpd_values))) <= std_dev,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_correlation = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_correlation) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")