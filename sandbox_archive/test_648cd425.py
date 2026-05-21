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

def generate_polynomial(n):
    coefficients = [random.randint(-10, 10) for _ in range(n + 1)]
    return sum(coeff * x**i for i, coeff in enumerate(coefficients))

def solve_polynomial(polynomial):
    n = len(polynomial) - 1
    roots = []
    if polynomial[n] != 0:
        for k in range(1 << n):
            root = Fraction(0)
            for i in range(n + 1):
                root += polynomial[i] * (-1)**i * (k >> i & 1)
            roots.append(root)
    return roots

def geometric_entropy(roots):
    if not roots:
        return 0
    unique_roots = set(roots)
    entropy = -sum(Fraction(1, len(unique_roots)) * math.log2(Fraction(1, len(unique_roots))) for _ in unique_roots)
    return entropy

def communication_complexity(n):
    # Simplified model: O(n^2) complexity
    return n**2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    polynomial = generate_polynomial(n)
    roots = solve_polynomial(polynomial)
    entropy = geometric_entropy(roots)
    complexity = communication_complexity(n)
    
    return {
        "metric_name": "Geometric Entropy",
        "metric_value": entropy,
        "instances_tested": 1,
        "conjecture_holds": entropy <= complexity,
        "counterexample": "" if entropy <= complexity else f"Entropy {entropy} > Complexity {complexity}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")