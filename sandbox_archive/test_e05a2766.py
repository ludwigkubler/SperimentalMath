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

def polynomial_degree(circuit, n):
    degree = 0
    for term in circuit:
        if isinstance(term, list):  # Check if term is a list (polynomial)
            degree = max(degree, sum(abs(coeff) * (n ** exp) for coeff, exp in term))
    return degree

def generate_xor_and_tree(n):
    if n == 1:
        return [[0], [1]]
    else:
        left = generate_xor_and_tree(n // 2)
        right = generate_xor_and_tree(n - n // 2)
        xor_terms = []
        and_terms = []
        for l in left:
            for r in right:
                xor_terms.append([l[0] ^ r[0]])
                and_terms.append([l[0] & r[0]])
        return xor_terms + and_terms

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    circuit = generate_xor_and_tree(n)
    degree = polynomial_degree(circuit, n)
    
    metric_name = "polynomial_degree"
    metric_value = degree
    instances_tested = 1
    conjecture_holds = degree >= math.log2(n)
    counterexample = "" if conjecture_holds else f"degree={degree}, expected=Ω(log {n})"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='degree less than Ω(log n)' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or budget exceeded")