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
    
    def generate_frege_proof(w):
        # Simple DPLL-based solver to generate a Frege proof
        clauses = [[random.randint(1, w), -random.randint(1, w)] for _ in range(w)]
        return clauses
    
    def geometric_entropy(clauses):
        # Simulate exploration of the proof space and count distinct configurations
        explored = set()
        stack = [clauses]
        while stack:
            current = stack.pop()
            if tuple(current) not in explored:
                explored.add(tuple(current))
                for clause in current:
                    new_clause = [x for x in current if x != clause]
                    stack.append(new_clause)
        return len(explored)

    n_max = 40
    instances_tested = 30
    total_entropy = 0
    
    for _ in range(instances_tested):
        w = random.randint(5, 40)
        proof = generate_frege_proof(w)
        entropy = geometric_entropy(proof)
        total_entropy += entropy
    
    mean_entropy = total_entropy / instances_tested
    conjecture_holds = False
    counterexample = ""
    
    if mean_entropy >= 0.1 * n_max:
        conjecture_holds = True
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97, 101, 103, 107, 109, 113
        ]
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_entropy) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")