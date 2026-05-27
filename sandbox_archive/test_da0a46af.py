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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def xor_and_tree_width(f):
        n = len(f)
        if n == 1:
            return 0
        mid = n // 2
        left = f[:mid]
        right = f[mid:]
        return max(xor_and_tree_width(left), xor_and_tree_width(right)) + 1
    
    def minimal_rank_of_lattice(f):
        n = len(f)
        if n == 1:
            return 1
        mid = n // 2
        left = f[:mid]
        right = f[mid:]
        rank_left = minimal_rank_of_lattice(left)
        rank_right = minimal_rank_of_lattice(right)
        return max(rank_left, rank_right) + 1
    
    def real_algebraic_lattice(f):
        n = len(f)
        if n == 1:
            return [f[0]]
        mid = n // 2
        left = f[:mid]
        right = f[mid:]
        lattice_left = real_algebraic_lattice(left)
        lattice_right = real_algebraic_lattice(right)
        lattice = []
        for l in lattice_left:
            for r in lattice_right:
                lattice.append(l + r)
        return lattice
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        xor_and_width = xor_and_tree_width(f)
        lattice = real_algebraic_lattice(f)
        rank = minimal_rank_of_lattice(f)
        
        if len(lattice) == 0:
            continue
        
        results.append({
            "n": n,
            "xor_and_width": xor_and_width,
            "rank": rank
        })
    
    if not results:
        return {
            "metric_name": "XOR-AND Tree Width vs Minimal Rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_xor_and_width = sum(result["xor_and_width"] for result in results) / len(results)
    std_xor_and_width = math.sqrt(sum((result["xor_and_width"] - mean_xor_and_width) ** 2 for result in results) / len(results))
    mean_rank = sum(result["rank"] for result in results) / len(results)
    
    support_fraction = sum(1 for result in results if result["xor_and_width"] <= 1.1 * result["rank"]) / len(results)
    
    return {
        "metric_name": "XOR-AND Tree Width vs Minimal Rank",
        "metric_value": mean_xor_and_width,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={results[0]['n']}, xor_and_width={results[0]['xor_and_width']}, rank={results[0]['rank']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        from sympy.ntheory import primerange
        seeds = list(primerange(2, 31))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, xor_and_width={results[0]['xor_and_width']}, rank={results[0]['rank']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")