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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def construct_root_lattice(edges):
        rank = len(edges)
        lattice = [[0] * rank for _ in range(rank)]
        for i, j in edges:
            lattice[i][j] = 1
            lattice[j][i] = 1
        return lattice
    
    def compute_geometric_entropy(lattice):
        n = len(lattice)
        det = 1
        for i in range(n):
            sum_row = sum(lattice[i])
            if sum_row == 0:
                continue
            det *= math.factorial(sum_row) / (math.factorial(sum_row - 2) * math.sqrt(2))
        return math.log(det)
    
    def compute_communication_complexity(edges):
        n = len(edges)
        return n * (n - 1) // 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph_edges = generate_random_graph(n)
        lattice = construct_root_lattice(graph_edges)
        H_R = compute_geometric_entropy(lattice)
        C = compute_communication_complexity(graph_edges)
        
        if H_R > C + 10 or (sum(abs(H_R - C) for _ in range(30)) / 30) > 5:
            return {
                "metric_name": "H(R) vs C",
                "metric_value": H_R,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, H(R)={H_R}, C={C}"
            }
    
    return {
        "metric_name": "H(R) vs C",
        "metric_value": (sum(compute_geometric_entropy(construct_root_lattice(generate_random_graph(n))) for n in n_values) / len(n_values)),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r - mean) <= 3) / len(results)
    
    if all(abs(r - mean) <= 3 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(abs(r - mean) > 10 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if abs(r - mean) > 10)
        print(f"RESULT: FALSIFIED counterexample=\"n={n_values[first_failing_seed]}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")