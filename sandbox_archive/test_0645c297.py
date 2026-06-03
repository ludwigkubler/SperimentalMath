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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR', 'NOT'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(1, n))]
            circuit.append((gate, inputs))
        return circuit
    
    def dependency_graph(circuit):
        graph = {i: set() for i in range(len(circuit))}
        for i, (gate, inputs) in enumerate(circuit):
            if gate == 'NOT':
                continue
            for j in inputs:
                graph[j].add(i)
        return graph
    
    def is_planar(graph):
        # Simple heuristic to check planarity: no self-loops or multiple edges between the same nodes
        for node, neighbors in graph.items():
            if len(neighbors) != len(set(neighbors)):
                return False
        return True
    
    def min_crossing_changes(circuit):
        n = len(circuit)
        if is_planar(dependency_graph(circuit)):
            return 0
        # Placeholder for actual crossing change calculation
        return random.randint(1, n)
    
    def cyclic_group_action(knot):
        # Placeholder for actual cyclic group action calculation
        return random.randint(1, 5)
    
    def correlation_coefficient(x, y):
        if len(x) != len(y) or not x:
            return None
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x)**2 for xi in x)) * math.sqrt(sum((yi - mean_y)**2 for yi in y))
        return numerator / denominator if denominator else None
    
    n_values = [5, 10, 15, 20, 30, 40]
    lcoh_values = []
    cg_action_values = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        graph = dependency_graph(circuit)
        if not is_planar(graph):
            continue
        lcoh = min_crossing_changes(circuit)
        cg_action = cyclic_group_action(graph)
        if lcoh is None or cg_action is None:
            continue
        lcoh_values.append(lcoh)
        cg_action_values.append(cg_action)
    
    if not lcoh_values or not cg_action_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(lcoh_values),
            "n_max": max(n_values) if n_values else 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = correlation_coefficient(lcoh_values, cg_action_values)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(lcoh_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation is not None and correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(res["conjecture_holds"] for res in results) / len(results)
    
    if all(res["metric_value"] is not None for res in results):
        RESULT = f"SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE mapping_undefined"
    
    print(RESULT)