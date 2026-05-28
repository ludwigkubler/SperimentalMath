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
    
    def generate_circuit(n, s):
        if n == 1:
            return [('AND', [0])]
        else:
            left = generate_circuit(n // 2, s // 2)
            right = generate_circuit(n - n // 2, s - s // 2)
            return [('OR', [left, right])]
    
    def vertex_cover(circuit):
        if not circuit:
            return 0
        gate, inputs = circuit[0]
        if gate == 'AND':
            return 1 + max(vertex_cover(inputs[0]), vertex_cover(inputs[1]))
        elif gate == 'OR':
            return 1 + min(vertex_cover(inputs[0]), vertex_cover(inputs[1]))
    
    def count_reduced_words(circuit):
        if not circuit:
            return 1
        gate, inputs = circuit[0]
        if gate == 'AND':
            return count_reduced_words(inputs[0]) * count_reduced_words(inputs[1])
        elif gate == 'OR':
            return count_reduced_words(inputs[0]) + count_reduced_words(inputs[1])
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        s_values = [min(s, n * (n - 1) // 2) for s in range(1, n * (n - 1) // 2 + 1)]
        for s in s_values:
            circuit = generate_circuit(n, s)
            num_vertices = vertex_cover(circuit)
            num_reduced_words = count_reduced_words(circuit)
            results.append({
                "metric_name": "vertex_cover_size",
                "metric_value": num_vertices,
                "instances_tested": 1,
                "conjecture_holds": num_vertices <= s ** (1/3),
                "counterexample": ""
            })
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_vertex_cover_size": mean_value,
        "std_vertex_cover_size": std_value,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["mean_vertex_cover_size"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["mean_vertex_cover_size"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] == 1) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["support_fraction"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["support_fraction"])
        counterexample = "vertex_cover_size"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")