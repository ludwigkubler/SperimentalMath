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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def config_space(graph):
        n = len(graph)
        rank = 0
        for subset in range(1 << n):
            subgraph = {edge for edge in graph if all(edge[i] in (subset >> i) & 1 for i in range(n))}
            if not subgraph:
                continue
            rank += 1
        return rank
    
    def communication_complexity(graph):
        n = len(graph)
        max_bits = 0
        for subset1 in range(1 << n):
            for subset2 in range(1 << n):
                if (subset1 & subset2) == 0:
                    bits = int(math.ceil(math.log2(n)))
                    max_bits = max(max_bits, bits)
        return max_bits
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_complexity = 0
    instances_tested = 0
    
    for n in n_values:
        graph = generate_graph(n)
        rank = config_space(graph)
        complexity = communication_complexity(graph)
        if rank == 0 or complexity == 0:
            continue
        total_rank += rank
        total_complexity += complexity
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    ratio = Fraction(total_rank, total_complexity)
    conjecture_holds = ratio <= Fraction(1.5 * n_values[-1], n_values[-1])
    counterexample = "" if conjecture_holds else f"ratio={ratio}, expected<=1.5*{n_values[-1]}/{n_values[-1]}"
    
    return {
        "metric_name": "ratio",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30)) + [67, 71, 73, 79, 83]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")