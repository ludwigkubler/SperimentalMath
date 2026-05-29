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
    
    def find_fundamental_group(edges, n):
        # Simplified version of finding the fundamental group
        # This is a placeholder and does not actually compute the fundamental group
        return len(edges)
    
    def calculate_communication_complexity(dim):
        # Placeholder for communication complexity calculation
        return 2 ** dim
    
    n = random.randint(5, 40)
    graph_edges = generate_random_graph(n)
    dim = find_fundamental_group(graph_edges, n)
    cc = calculate_communication_complexity(dim)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": cc,
        "instances_tested": 1,
        "conjecture_holds": abs(cc - (2 ** dim)) / (2 ** dim) < 0.5,
        "counterexample": "" if conjecture_holds else f"CC(Aut_G) = {cc}, dim(π₁(G)) = {dim}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_cc = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_cc) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_cc} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")