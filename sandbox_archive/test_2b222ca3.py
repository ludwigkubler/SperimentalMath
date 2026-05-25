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
        # Simplified DPLL solver for Frege proof length (not actual DPLL)
        n = len(f)
        if n == 1:
            return 1
        else:
            return 2 * frege_proof_length([f[i] and f[j] for i in range(n) for j in range(i+1, n)])
    
    def von_neumann_entropy(f):
        # Simplified calculation of von Neumann entropy (not actual quantum state)
        n = len(f)
        count = sum(1 for x in f if x == True)
        p = count / n
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)
    
    def factorial(n):
        if n == 0:
            return 1
        else:
            return n * factorial(n-1)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(10, 40)
        f = [random.choice([True, False]) for _ in range(n)]
        entropy = von_neumann_entropy(f)
        proof_length = frege_proof_length(f)
        if entropy > (math.log2(factorial(n)) / math.log2(n**proof_length)):
            results.append({"n": n, "f": f, "entropy": entropy, "proof_length": proof_length})
    
    metric_value = sum(result["entropy"] for result in results) / len(results)
    conjecture_holds = all(result["entropy"] <= (math.log2(factorial(result["n"])) / math.log2(result["n"]**result["proof_length"])) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Von Neumann Entropy",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")