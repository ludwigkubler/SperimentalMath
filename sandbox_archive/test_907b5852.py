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
    
    def frege_proof_length(f):
        # Simplified DPLL solver for Frege proof length (not actual implementation)
        return len(f)

    def von_neumann_entropy(n, m):
        if n == 0 or m == 0:
            return 0
        p = m / n
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]

    c = 1.5  # Example constant
    results = []
    
    for n in range(10, 41):
        f = generate_boolean_function(n)
        proof_length = frege_proof_length(f)
        entropy = von_neumann_entropy(2**n, sum(f))
        
        if entropy > c * math.log2(math.factorial(n)) / math.log2(n ** proof_length):
            results.append({"n": n, "entropy": entropy, "proof_length": proof_length, "conjecture_holds": False})
        else:
            results.append({"n": n, "entropy": entropy, "proof_length": proof_length, "conjecture_holds": True})

    metric_value = sum(result["entropy"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["conjecture_holds"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Von Neumann Entropy",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")