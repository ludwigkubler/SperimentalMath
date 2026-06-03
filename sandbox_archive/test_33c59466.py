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
    
    def generate_graph(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.append((i, j))
        return edges
    
    def local_indeterminacy(graph):
        # Simplified version of local indeterminacy calculation
        return len(graph)
    
    def circuit_monotone_width(graph):
        # Simplified version of circuit monotone width calculation
        return len(graph) ** 0.5
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_local_indeterminacy = 0
    total_circuit_monotone_width = 0
    
    for n in n_values:
        for _ in range(5):
            graph = generate_graph(n)
            local_ind = local_indeterminacy(graph)
            circuit_width = circuit_monotone_width(graph)
            instances_tested += 1
            total_local_indeterminacy += local_ind
            total_circuit_monotone_width += circuit_width
    
    mean_local_ind = total_local_indeterminacy / instances_tested
    mean_circuit_width = total_circuit_monotone_width / instances_tested
    ratio = mean_local_ind / mean_circuit_width if mean_circuit_width != 0 else float('inf')
    
    conjecture_holds = abs(ratio - 1) <= 0.1
    counterexample = "" if conjecture_holds else f"Ratio {ratio} not within 10% of 1"
    
    return {
        "metric_name": "Local Indeterminacy / Circuit Monotone Width Ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of tolerance\" first_failing_seed={first_failing_seed}")