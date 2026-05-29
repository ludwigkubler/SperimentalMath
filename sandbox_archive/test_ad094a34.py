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
    
    def zeta(s):
        if s <= 1:
            return float('inf')
        return sum(1 / (i ** s) for i in range(1, 1000))  # Approximation
    
    def branching_program_size(f, n):
        if len(f) != 2**n:
            return None
        nodes = [set() for _ in range(n + 1)]
        nodes[0].add((f, 0))
        for i in range(1, n + 1):
            new_nodes = set()
            for node in nodes[i - 1]:
                val, idx = node
                if idx < len(val) - 1:
                    left_node = (val[:idx] + '0' + val[idx+1:], idx + 1)
                    right_node = (val[:idx] + '1' + val[idx+1:], idx + 1)
                    new_nodes.add(left_node)
                    new_nodes.add(right_node)
            nodes[i] = new_nodes
        return len(nodes[n])
    
    n = 40
    f = generate_boolean_function(n)
    zeta_value = zeta(0.5)  # Approximation of ζ(1/2)
    size = branching_program_size(f, n)
    
    metric_name = "branching_program_size"
    metric_value = size if size is not None else float('inf')
    instances_tested = 1
    conjecture_holds = False if zeta_value == float('inf') or size > n**(3/4) * 2 else True
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")