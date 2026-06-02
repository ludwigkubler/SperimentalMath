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
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0 or d > n - 1:
            return None
        graph = [[0] * n for _ in range(n)]
        for i in range(d):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    graph[i][j] = 1
                    graph[j][i] = 1
        return graph
    
    def compute_automorphic_representation(graph):
        # Placeholder function to simulate computation of automorphic representation
        return sum(sum(row) for row in graph)
    
    def calculate_min_index(automorphic_representation):
        # Placeholder function to simulate calculation of minimal index
        return abs(automorphic_representation)
    
    def construct_circuit_representation(graph):
        # Placeholder function to simulate construction of circuit representation
        return len(graph)
    
    def compute_monotone_width(circuit_representation):
        # Placeholder function to simulate computation of monotone width
        return sum(len(row) for row in circuit_representation)
    
    n = 40
    d = random.randint(1, n - 2)
    graph = generate_d_regular_graph(n, d)
    if not graph:
        return {
            "metric_name": "min_index",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Failed to generate a valid d-regular graph"
        }
    
    automorphic_representation = compute_automorphic_representation(graph)
    min_index = calculate_min_index(automorphic_representation)
    circuit_representation = construct_circuit_representation(graph)
    monotone_width = compute_monotone_width(circuit_representation)
    
    return {
        "metric_name": "min_index",
        "metric_value": min_index,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")