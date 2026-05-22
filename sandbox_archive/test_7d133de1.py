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
    
    def generate_k_clique(n: int, k: int):
        if n < k:
            return []
        vertices = list(range(n))
        clique_edges = [(u, v) for u in range(k) for v in range(u + 1, k)]
        remaining_edges = [(u, v) for u in range(k, n) for v in range(u + 1, n) if (u, v) not in clique_edges]
        random.shuffle(remaining_edges)
        edges = clique_edges + remaining_edges[:n - k]
        return vertices, edges
    
    def matroid_rank(edges):
        n = len(edges)
        if n == 0:
            return 0
        rank = 1
        for i in range(n):
            new_edge = edges[i]
            if all((new_edge[0] != edge[0] and new_edge[0] != edge[1]) or (new_edge[1] != edge[0] and new_edge[1] != edge[1]) for edge in edges[:i]):
                rank += 1
        return rank
    
    def monotone_circuit_size(k):
        # Upper bound on the size of a monotone circuit computing k-CLIQUE
        return math.factorial(k) * math.log2(math.factorial(k))
    
    n = random.randint(5, 40)
    k = random.randint(3, min(n - 1, 8))
    vertices, edges = generate_k_clique(n, k)
    rank = matroid_rank(edges)
    circuit_size = monotone_circuit_size(k)
    
    return {
        "metric_name": "matroid_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= circuit_size,
        "counterexample": "" if rank >= circuit_size else f"rank={rank} < {circuit_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank < monotone circuit size\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")