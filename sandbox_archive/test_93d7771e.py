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
    
    def generate_tseitin_circuit(n):
        if n == 1:
            return "x"
        else:
            a = generate_tseitin_circuit(n // 2)
            b = generate_tseitin_circuit(n - n // 2)
            return f"({a} | {b})"
    
    def construct_quasi_vertex_descent_tree(circuit):
        if isinstance(circuit, str):
            return circuit
        else:
            left = construct_quasi_vertex_descent_tree(circuit[0])
            right = construct_quasi_vertex_descent_tree(circuit[2])
            return f"({left} {circuit[1]} {right})"
    
    def calculate_minimal_rank(tree):
        if isinstance(tree, str):
            return 1
        else:
            left_rank = calculate_minimal_rank(tree[0])
            right_rank = calculate_minimal_rank(tree[2])
            return max(left_rank, right_rank) + 1
    
    n = random.randint(5, 40)
    circuit = generate_tseitin_circuit(n)
    tree = construct_quasi_vertex_descent_tree(circuit)
    minimal_rank = calculate_minimal_rank(tree)
    
    expected_rank = 2 ** (0.5 * math.log2(n))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": minimal_rank >= expected_rank,
        "counterexample": "" if minimal_rank >= expected_rank else f"rank={minimal_rank}, expected={expected_rank}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")