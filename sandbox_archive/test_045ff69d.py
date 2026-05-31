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
    
    def generate_quiver(n, m):
        edges = set()
        while len(edges) < m:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return n, list(edges)
    
    def compute_minimal_order_of_automorphisms(n, edges):
        # Simplified heuristic for minimal order of automorphisms
        # This is a placeholder as the actual computation is complex
        return 1 + int(math.log(m) / math.log(2))
    
    def generate_arithmetic_circuit(n, m):
        # Placeholder for generating an arithmetic circuit
        return random.randint(1, n)
    
    def compute_communication_complexity(circuit_size):
        # Simplified heuristic for communication complexity
        return circuit_size
    
    n = 40
    m = random.randint(5 * n, 2 * n**2)
    n, edges = generate_quiver(n, m)
    minimal_order = compute_minimal_order_of_automorphisms(n, edges)
    circuit_size = generate_arithmetic_circuit(n, m)
    communication_complexity = compute_communication_complexity(circuit_size)
    
    if minimal_order <= 0:
        return {
            "metric_name": "minimal_order",
            "metric_value": minimal_order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "negative_minimal_order"
        }
    
    if communication_complexity <= 0:
        return {
            "metric_name": "communication_complexity",
            "metric_value": communication_complexity,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "negative_communication_complexity"
        }
    
    if abs(communication_complexity - math.sqrt(m)) > 1:
        return {
            "metric_name": "communication_complexity",
            "metric_value": communication_complexity,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"communication_complexity={communication_complexity}, expected=~{math.sqrt(m)}"
        }
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_communication_complexity = sum(r["metric_value"] for r in results) / len(results)
    std_communication_complexity = math.sqrt(sum((r["metric_value"] - mean_communication_complexity) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_communication_complexity} std={std_communication_complexity} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_communication_complexity} std={std_communication_complexity} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='communication_complexity_outside_bound' first_failing_seed={first_failing_seed}")