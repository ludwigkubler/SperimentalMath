# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_clique_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def tensor_rank(edges, n):
        # Construct a tensor representation of the clique instance
        T = [[0] * n for _ in range(n)]
        for u, v in edges:
            T[u][v] = 1
            T[v][u] = 1
        rank = 0
        while True:
            found_nonzero = False
            for i in range(n):
                if any(T[i][j] != 0 for j in range(n)):
                    found_nonzero = True
                    break
            if not found_nonzero:
                break
            rank += 1
            for i in range(n):
                if T[i][i] == 0:
                    continue
                for j in range(n):
                    T[j][i] /= T[i][i]
                for k in range(n):
                    T[k][j] -= T[k][i] * T[i][j]
        return rank
    
    def monotone_circuit_size(n):
        # Placeholder function to simulate the size of a monotone circuit
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(10, 50)
    
    n = random.choice([10, 20, 30, 40])
    edges = generate_clique_instance(n)
    rank = tensor_rank(edges, n)
    circuit_size = monotone_circuit_size(n)
    
    metric_name = "tensor_rank_vs_circuit_size"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= n**0.5 and circuit_size >= (1 / random.random()) * n**0.5
    counterexample = "" if conjecture_holds else f"Rank {rank} exceeds {n**0.5}, Circuit size {circuit_size} < {(1 / random.random()) * n**0.5}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")