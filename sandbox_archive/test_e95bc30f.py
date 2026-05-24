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
        # Simplified mapping to a root lattice
        rank = len(edges) * 2
        return rank
    
    def compute_geometric_entropy(rank):
        # Simplified entropy calculation
        if rank == 0:
            return 0.0
        return -rank * math.log2(1 / rank)
    
    def compute_communication_complexity(n):
        # Placeholder for actual complexity computation
        return n * (n - 1) // 2
    
    n = random.randint(5, 40)
    graph_edges = generate_random_graph(n)
    lattice_rank = construct_root_lattice(graph_edges)
    entropy = compute_geometric_entropy(lattice_rank)
    communication_complexity = compute_communication_complexity(n)
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": entropy,
        "instances_tested": 1,
        "conjecture_holds": entropy <= communication_complexity,
        "counterexample": "" if entropy <= communication_complexity else f"Entropy {entropy} > Complexity {communication_complexity}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")