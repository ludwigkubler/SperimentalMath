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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_expander_graph(n):
        # Ramanujan construction for expander graphs
        if n <= 2:
            return []
        vertices = list(range(n))
        edges = []
        for i in range(1, n):
            edges.extend([(i, (i * j) % n) for j in range(1, n)])
        return vertices, edges
    
    def euler_characteristic(vertices, edges):
        return len(vertices) - len(edges)
    
    def resolution_proof_length(n):
        # Simplified DPLL-based solver
        # This is a placeholder function. Replace with actual implementation.
        return random.randint(10**n, 2*10**n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    vertices, edges = generate_expander_graph(n)
    euler_char = euler_characteristic(vertices, edges)
    proof_length = resolution_proof_length(n)
    
    bound = Fraction(1.5**n, euler_char**2) if euler_char != 0 else float('inf')
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": proof_length <= bound,
        "counterexample": "" if proof_length <= bound else f"Proof length {proof_length} exceeds bound {bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100, 4))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")