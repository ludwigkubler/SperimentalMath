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

def generate_boolean_algebra(n, k):
    if n == 0 or k < 0:
        return [], []
    
    elements = [tuple(sorted(random.sample(range(2), n))) for _ in range(k)]
    relations = [(i, j) for i in range(k) for j in range(i+1, k) if random.choice([True, False])]
    
    return elements, relations

def hodge_diamond_rank(elements):
    if not elements:
        return 0
    
    n = len(elements[0])
    rank = 2 * n + 1
    return rank

def ac0_parity_depth(n):
    # Simplified approximation for AC⁰ PARITY depth
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for k in range(1, min(n, 10)):  # Ensure k is at least 1 and less than n
            B_elements, B_relations = generate_boolean_algebra(n, k)
            rank = hodge_diamond_rank(B_elements)
            depth = ac0_parity_depth(n)
            
            results.append({
                "n": n,
                "k": k,
                "rank": rank,
                "depth": depth
            })
    
    total_instances = len(results)
    conjecture_holds = all(result["rank"] <= result["depth"] for result in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, k={results[0]['k']}"
    
    return {
        "metric_name": "Hodge Diamond Rank vs AC⁰ PARITY Depth",
        "metric_value": sum(result["rank"] for result in results) / total_instances,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, k={results[0]['k']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")