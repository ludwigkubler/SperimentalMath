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
    
    def generate_circuit(n):
        circuit = []
        for _ in range(n):
            gate = random.choice(['XOR', 'AND'])
            circuit.append(gate)
        return circuit
    
    def group_representation(circuit):
        G = {0, 1}  # Cyclic group of order 2
        for gate in circuit:
            if gate == 'XOR':
                G = {x ^ y for x in G for y in G}
            elif gate == 'AND':
                G = {x & y for x in G for y in G}
        return len(G)
    
    def entanglement(circuit):
        # Simplified entanglement measure for demonstration
        return len(circuit) / 2
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_circuit(n)
        min_order = group_representation(circuit)
        epsilon = entanglement(circuit)
        metric_values.append((min_order, epsilon))
    
    if not metric_values:
        return {
            "metric_name": "min_order vs. entanglement",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No circuits generated"
        }
    
    min_orders = [v[0] for v in metric_values]
    epsilons = [v[1] for v in metric_values]
    
    mean_min_order = sum(min_orders) / len(min_orders)
    mean_epsilon = sum(epsilons) / len(epsilons)
    correlation_coefficient = 0
    
    if len(min_orders) > 1:
        numerator = sum((min_orders[i] - mean_min_order) * (epsilons[i] - mean_epsilon) for i in range(len(min_orders)))
        denominator = math.sqrt(sum((min_orders[i] - mean_min_order) ** 2 for i in range(len(min_orders)))) * math.sqrt(sum((epsilons[i] - mean_epsilon) ** 2 for i in range(len(epsilons))))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "Correlation coefficient < 0.8"
    
    return {
        "metric_name": "min_order vs. entanglement",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and min(r["metric_value"] for r in results if not r["conjecture_holds"]) >= 0.5:
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8\" first_failing_seed={next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'] and result['metric_value'] >= 0.5)}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")