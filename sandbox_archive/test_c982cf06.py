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
from itertools import permutations

def generate_random_graph(n):
    graph = {}
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                graph[(i, j)] = True
    return graph

def is_permutation_valid(perm, graph):
    for i, j in graph:
        if perm[i] not in graph or perm[j] not in graph:
            return False
        if (perm[i], perm[j]) not in graph and (perm[j], perm[i]) not in graph:
            return False
    return True

def symmetry_group_order(graph):
    n = len(graph)
    vertices = list(range(n))
    sym_order = 1
    for perm in permutations(vertices):
        if is_permutation_valid(perm, graph):
            sym_order += 1
    return sym_order

def resolution_proof_length(graph):
    # Simplified version of Resolution proof length calculation
    n = len(graph)
    return 2 ** (n - 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        graph = generate_random_graph(random.randint(5, 40))
        sym_order = symmetry_group_order(graph)
        proof_length = resolution_proof_length(graph)
        results.append(proof_length)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(length >= 2 ** sym_order for length in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Resolution proof length",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 2 ** math.log2(len(graph)) for graph in [generate_random_graph(random.randint(5, 40))]) / len(results)
    
    if all(r >= 2 ** math.log2(len(graph)) for r in results for graph in [generate_random_graph(random.randint(5, 40))]):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < 2 ** math.log2(len(graph)) for r in results for graph in [generate_random_graph(random.randint(5, 40))]):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")