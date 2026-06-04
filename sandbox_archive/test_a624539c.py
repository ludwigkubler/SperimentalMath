# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n, m):
        gates = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), 2)
            gates.append((gate_type, inputs))
        return gates
    
    def is_subgroup(H, G):
        if not H:
            return True
        if len(H) > len(G):
            return False
        for h in H:
            if h not in G:
                return False
        return all(is_subgroup(generate_circuit(len(h), 1)[0], G) for g in H)
    
    def find_largest_subgroup(circuit):
        n = len(circuit[0][1])
        elements = list(range(n))
        largest_subgroup = []
        for r in range(1, len(elements)):
            for subset in combinations(elements, r):
                subgroup = generate_circuit(r, 1)[0]
                if is_subgroup(subgroup, circuit):
                    largest_subgroup = subgroup
        return largest_subgroup
    
    def compute_symmetry_group_order(circuit):
        n = len(circuit[0][1])
        elements = list(range(n))
        order = 1
        for r in range(1, len(elements)):
            for subset in combinations(elements, r):
                subgroup = generate_circuit(r, 1)[0]
                if is_subgroup(subgroup, circuit):
                    order *= math.factorial(len(subset))
        return order
    
    def compute_monotone_width(circuit):
        n = len(circuit[0][1])
        width = 0
        for i in range(n):
            for j in range(i + 1, n):
                if all(gate[0] == 'AND' and gate[1] == (i, j) for gate in circuit):
                    width += 1
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_symmetry_group_order = 0
    total_monotone_width = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n, random.randint(2 * n, 3 * n))
            symmetry_group_order = compute_symmetry_group_order(circuit)
            monotone_width = compute_monotone_width(circuit)
            
            total_symmetry_group_order += symmetry_group_order
            total_monotone_width += monotone_width
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_symmetry_group_order = total_symmetry_group_order / instances_tested
    mean_monotone_width = total_monotone_width / instances_tested
    
    if instances_tested < 30:
        return {
            "metric_name": "symmetry_group_order",
            "metric_value": mean_symmetry_group_order,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    covariance = 0
    variance_symmetry_group_order = 0
    variance_monotone_width = 0
    
    for _ in range(5):
        circuit = generate_circuit(n_max, random.randint(2 * n_max, 3 * n_max))
        symmetry_group_order = compute_symmetry_group_order(circuit)
        monotone_width = compute_monotone_width(circuit)
        
        covariance += (symmetry_group_order - mean_symmetry_group_order) * (monotone_width - mean_monotone_width)
        variance_symmetry_group_order += (symmetry_group_order - mean_symmetry_group_order) ** 2
        variance_monotone_width += (monotone_width - mean_monotone_width) ** 2
    
    covariance /= 5
    variance_symmetry_group_order /= 5
    variance_monotone_width /= 5
    
    if variance_symmetry_group_order == 0 or variance_monotone_width == 0:
        return {
            "metric_name": "symmetry_group_order",
            "metric_value": mean_symmetry_group_order,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_symmetry_group_order) * math.sqrt(variance_monotone_width))
    
    return {
        "metric_name": "symmetry_group_order",
        "metric_value": mean_symmetry_group_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")