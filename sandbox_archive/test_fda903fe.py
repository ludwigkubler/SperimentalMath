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
        G = {0, 1}
        for gate in circuit:
            if gate == 'XOR':
                G = {x ^ y for x in G for y in G}
            elif gate == 'AND':
                G = {x & y for x in G for y in G}
        return len(G)
    
    def concurrence(state):
        # Simplified concurrence calculation for a 2-qubit state
        rho = state[0][0] * state[1][1] + state[0][1] * state[1][0]
        return 2 * abs(rho) ** 2
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_circuit(n)
        min_order = group_representation(circuit)
        
        # Simulate a quantum state (simplified)
        state = [[random.random(), random.random()], [random.random(), random.random()]]
        entanglement = concurrence(state)
        
        metric_values.append((min_order, entanglement))
    
    if not metric_values:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No data generated"
        }
    
    min_orders = [val[0] for val in metric_values]
    entanglements = [val[1] for val in metric_values]
    
    mean_min_order = sum(min_orders) / instances_tested
    mean_entanglement = sum(entanglements) / instances_tested
    
    correlation_coefficient = 0.0
    if len(set(min_orders)) > 1 and len(set(entanglements)) > 1:
        numerator = sum((min_orders[i] - mean_min_order) * (entanglements[i] - mean_entanglement) for i in range(instances_tested))
        denominator = math.sqrt(sum((min_orders[i] - mean_min_order) ** 2 for i in range(instances_tested))) * math.sqrt(sum((entanglements[i] - mean_entanglement) ** 2 for i in range(instances_tested)))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(cc >= 0.5 for cc in [correlation_coefficient]),
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient {correlation_coefficient} < 0.8"
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] and res["metric_value"] < 0.5 for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"] and res["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient below 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")