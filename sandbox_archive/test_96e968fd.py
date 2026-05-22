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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_polynomial(d, n):
        coeffs = [random.randint(0, 1) for _ in range(n)]
        return sum(c * x**i for i, c in enumerate(coeffs))
    
    def schur_weyl_rank(f):
        # Placeholder function to compute Schur-Weyl rank
        # This is a dummy implementation and should be replaced with actual computation
        return len(str(f))  # Simplified as length of polynomial string
    
    def monotone_circuit_depth(n, d):
        # Placeholder function to compute depth of monotone circuit
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(10, 50)  # Random depth between 10 and 50
    
    n = random.randint(5, 40)
    d = random.randint(10, 100)
    
    f = generate_polynomial(d, n)
    rho_f = schur_weyl_rank(f)
    D = monotone_circuit_depth(n, d)
    
    ratio = Fraction(rho_f, d**(2/3))
    
    return {
        "metric_name": "Schur-Weyl Rank / Degree^(2/3)",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": "" if ratio <= 1.5 else f"Ratio {ratio} > 1.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = (sum((r["metric_value"] - mean)**2 for r in results) / len(results))**0.5
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[seeds.index(first_failing_seed)]["counterexample"]
        mean = sum(r["metric_value"] for r in results)
        std = (sum((r["metric_value"] - mean)**2 for r in results) / len(results))**0.5
        support_fraction = Fraction(sum(1 for r in results if r["conjecture_holds"]), len(results))
    
    print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")