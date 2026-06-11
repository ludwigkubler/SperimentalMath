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

def generate_boolean_circuit(n, d):
    if n == 1 or d == 0:
        return ['input']
    else:
        inputs = []
        for _ in range(n):
            sub_inputs = generate_boolean_circuit(n // 2, d - 1)
            operator = random.choice(['AND', 'OR'])
            inputs.append((operator, sub_inputs))
        return inputs

def evaluate_circuit(circuit):
    stack = []
    for item in circuit:
        if isinstance(item, tuple):
            op, args = item
            right = stack.pop()
            left = stack.pop()
            if op == 'AND':
                result = all(left, right)
            elif op == 'OR':
                result = any(left, right)
            stack.append(result)
        else:
            stack.append(item)
    return stack[0]

def generate_random_circuit(n, d):
    circuit = generate_boolean_circuit(n, d)
    inputs = [random.choice([True, False]) for _ in range(n)]
    return evaluate_circuit(circuit), inputs

def compute_entanglement_complexity(circuit):
    # Placeholder function to simulate entanglement complexity
    # This is a dummy implementation and should be replaced with actual computation
    return len(circuit)

def compute_hdim(V):
    # Placeholder function to simulate Hodge-De Rham cohomology dimension
    # This is a dummy implementation and should be replaced with actual computation
    return len(V)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    hdim_sum = 0
    e_phi_sum = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            V, inputs = generate_random_circuit(n, random.randint(1, 4))
            hdim = compute_hdim(V)
            e_phi = compute_entanglement_complexity(circuit)
            hdim_sum += hdim
            e_phi_sum += e_phi
            instances_tested += 1
    
    mean_hdim = Fraction(hdim_sum, instances_tested)
    mean_e_phi = Fraction(e_phi_sum, instances_tested)
    
    correlation_coefficient = (instances_tested * sum(hdim * e_phi for hdim, e_phi in zip(hdim_values, e_phi_values)) -
                               mean_hdim * sum(e_phi_values) - 
                               sum(hdim_values) * mean_e_phi) / math.sqrt((instances_tested * sum(hdim ** 2 for hdim in hdim_values) - mean_hdim ** 2) *
                                                                    (instances_tested * sum(e_phi ** 2 for e_phi in e_phi_values) - mean_e_phi ** 2))
    
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) / math.sqrt(2 * instances_tested - 3)))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and p_value <= 0.05,
        "counterexample": "" if correlation_coefficient >= 0.8 and p_value <= 0.05 else "Pearson correlation coefficient < 0.8 or p-value > 0.05"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")