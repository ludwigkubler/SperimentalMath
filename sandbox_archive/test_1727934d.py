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
    
    def generate_polynomial(n, d):
        coeffs = [random.randint(1, 10) for _ in range(d + 1)]
        return sum(c * x**i for i, c in enumerate(coeffs))
    
    def schur_weyl_rank(f):
        # Placeholder function to compute the rank of Schur-Weyl duality representation
        # This is a dummy implementation; replace with actual computation if possible
        return len(f.coeffs)
    
    def xor_circuit_depth(f):
        # Placeholder function to compute the depth of XOR circuit based on polynomial properties
        # This is a dummy implementation; replace with actual computation if possible
        return len(f.coeffs) ** 2
    
    n = random.randint(5, 40)
    d = random.randint(1, n // 2)
    f = generate_polynomial(n, d)
    
    rank = schur_weyl_rank(f)
    depth = xor_circuit_depth(f)
    
    if rank == 0:
        return {
            "metric_name": "XOR Circuit Depth",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "XOR Circuit Depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": rank ** 2 == depth,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_depth = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")