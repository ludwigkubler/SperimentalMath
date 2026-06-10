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
    
    def generate_circuit(n, d):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            subcircuits = [generate_circuit(random.randint(1, n-1), random.randint(1, d-1)) for _ in range(d)]
            return [sum(subcircuit) % 2 for subcircuit in zip(*subcircuits)]
    
    def complement_graph(circuit):
        n = len(circuit)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if circuit[i] != circuit[j]:
                    G[i][j] = 1
                    G[j][i] = 1
        return G
    
    def min_rank(G):
        n = len(G)
        A = [list(row) for row in G]
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(i)):
                continue
            pivot_row = next(j for j in range(i, n) if A[j][i] != 0)
            A[i], A[pivot_row] = A[pivot_row], A[i]
            rank += 1
            for j in range(n):
                if i == j:
                    continue
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        return rank
    
    def d_to_n(d, n):
        return int((d ** (3/2)) * (n ** (1/3)))
    
    max_ratio = 0
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            d = random.randint(1, min(n, 40))
            circuit = generate_circuit(n, d)
            G = complement_graph(circuit)
            rank = min_rank(G)
            instances_tested += 1
            n_max = max(n_max, n)
            ratio = rank / d_to_n(d, n)
            if ratio > max_ratio:
                max_ratio = ratio
    
    conjecture_holds = max_ratio <= 2
    counterexample = "" if conjecture_holds else f"max_ratio={max_ratio}"
    
    return {
        "metric_name": "max_ratio",
        "metric_value": max_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_ratio exceeded\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence support_fraction={support_fraction}")