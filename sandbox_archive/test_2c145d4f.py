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
    
    def generate_circuit(n, m):
        circuit = []
        for _ in range(m):
            row = [random.randint(0, 1) for _ in range(n)]
            circuit.append(row)
        return circuit
    
    def is_monotone(circuit):
        n = len(circuit[0])
        m = len(circuit)
        for i in range(m):
            if not all(circuit[i][j] == circuit[0][j] for j in range(n)):
                return False
        return True
    
    def calculate_geometric_group_order(graph):
        # Placeholder implementation; actual computation depends on graph structure
        n = len(graph)
        order = 1
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == graph[j][i]:
                    order += 1
        return order
    
    def calculate_monotone_width(circuit):
        n = len(circuit[0])
        m = len(circuit)
        width = 0
        for i in range(m):
            width = max(width, circuit[i].count(1))
        return width
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        m = random.randint(n, n + 5)
        circuit = generate_circuit(n, m)
        if not is_monotone(circuit):
            continue
        graph = [[0] * n for _ in range(n)]
        for i in range(m):
            for j in range(n):
                if circuit[i][j] == 1:
                    graph[j][i] = 1
        
        geometric_group_order = calculate_geometric_group_order(graph)
        monotone_width = calculate_monotone_width(circuit)
        
        results.append((geometric_group_order, monotone_width))
    
    if not results:
        return {
            "metric_name": "Geometric Group Order vs Monotone Width",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No monotone circuits found"
        }
    
    geometric_group_orders = [r[0] for r in results]
    monotone_widths = [r[1] for r in results]
    
    mean_order = sum(geometric_group_orders) / len(geometric_group_orders)
    mean_width = sum(monotone_widths) / len(monotone_widths)
    std_order = math.sqrt(sum((x - mean_order) ** 2 for x in geometric_group_orders) / len(geometric_group_orders))
    std_width = math.sqrt(sum((x - mean_width) ** 2 for x in monotone_widths) / len(monotone_widths))
    
    correlation_coefficient = sum((x - mean_order) * (y - mean_width) for x, y in zip(geometric_group_orders, monotone_widths)) / (len(results) * std_order * std_width)
    
    return {
        "metric_name": "Geometric Group Order vs Monotone Width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")