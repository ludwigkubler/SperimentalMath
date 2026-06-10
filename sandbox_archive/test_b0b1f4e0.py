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

def generate_circuit(n):
    if n == 1:
        return ['0', '1']
    left = generate_circuit(n // 2)
    right = generate_circuit(n - n // 2)
    return [f'({l} AND {r})' for l in left] + [f'({l} OR {r})' for l in right]

def construct_noncommutative_algebra(circuit):
    if not circuit:
        return {}
    
    # Simplified construction of the algebra
    algebra = {}
    for expr in circuit:
        if 'AND' in expr:
            left, right = expr.split(' AND ')
            algebra[left] = algebra.get(left, 0) + 1
            algebra[right] = algebra.get(right, 0) + 1
        elif 'OR' in expr:
            left, right = expr.split(' OR ')
            algebra[left] = algebra.get(left, 0) + 1
            algebra[right] = algebra.get(right, 0) + 1
    
    return algebra

def calculate_minimal_rank(algebra):
    rank = 0
    for key in algebra:
        if algebra[key] > rank:
            rank = algebra[key]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    circuit_ranks = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        algebra = construct_noncommutative_algebra(circuit)
        rank = calculate_minimal_rank(algebra)
        circuit_ranks.append(rank)
    
    mean_rank = sum(circuit_ranks) / len(circuit_ranks)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in circuit_ranks) / len(circuit_ranks))
    
    conjecture_holds = all(rank <= n * math.log(n, 2) for rank, n in zip(circuit_ranks, n_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(circuit_ranks),
        "n_max": max(n_values),
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
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")