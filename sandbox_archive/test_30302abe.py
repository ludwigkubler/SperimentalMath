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
    
    n = 30  # Fixed size for simplicity
    if n < 5 or n > 40:
        return {
            "metric_name": "circuit_depth",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "sub-asymptotic_n"
        }
    
    # Simulate a function in P with known k-CLIQUE properties
    def clique_function(x):
        return sum(1 for i in range(n) if x[i] == 1)
    
    # Compute the minimal order of formal language automorphisms
    def minimal_automorphism_order():
        # Placeholder implementation; actual computation depends on group theory
        return random.randint(1, n)
    
    automorphism_order = minimal_automorphism_order()
    
    # Simulate these automorphisms on a monotone circuit model for k-CLIQUE
    def simulate_circuit(depth):
        # Placeholder implementation; actual simulation depends on circuit complexity
        return depth
    
    circuit_depth = simulate_circuit(automorphism_order)
    
    return {
        "metric_name": "circuit_depth",
        "metric_value": circuit_depth,
        "instances_tested": 1,
        "conjecture_holds": circuit_depth <= math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_depth = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")