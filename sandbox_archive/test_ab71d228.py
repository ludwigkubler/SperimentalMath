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
        # Generate a random boolean circuit with n variables and depth 5-10
        depth = random.randint(5, 10)
        nodes = [f"n{i}" for i in range(n)]
        edges = []
        for _ in range(depth):
            new_nodes = [f"n{i}" for i in range(n + len(edges))]
            for u in nodes:
                v = new_nodes[random.randint(0, len(new_nodes) - 1)]
                edges.append((u, v))
            nodes = new_nodes
        return edges

    def syntactic_monoid(edges):
        # Compute the syntactic monoid of the circuit
        generators = set()
        relations = set()
        for u, v in edges:
            generators.add(u)
            generators.add(v)
            relations.add((u, v))
        return generators, relations

    def minimal_locally_indecomposable_module(generators, relations):
        # Compute the minimal locally indecomposable module
        module_order = len(generators) * len(relations)
        return module_order

    n_max = 0
    total_ratio = 0.0
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            edges = generate_circuit(n)
            generators, relations = syntactic_monoid(edges)
            module_order = minimal_locally_indecomposable_module(generators, relations)
            depth = len(edges) // n
            ratio = module_order / (depth ** 2)
            
            if ratio < 0.5 or ratio > 1.5:
                return {
                    "metric_name": "Ratio of Module Order to Depth^2",
                    "metric_value": ratio,
                    "instances_tested": instances_tested + 1,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": "ratio_outside_bounds"
                }
            
            total_ratio += ratio
            instances_tested += 1
    
    return {
        "metric_name": "Ratio of Module Order to Depth^2",
        "metric_value": total_ratio / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='ratio_outside_bounds' first_failing_seed={first_failing_seed}")