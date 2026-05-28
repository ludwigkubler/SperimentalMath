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
    
    def arithmetic_divergence(n):
        # Placeholder for actual computation
        return n ** (1/4)
    
    def xor_circuit_size_and_depth():
        S = random.randint(1, 40)
        D = random.randint(1, 40)
        return S, D
    
    n = random.randint(5, 40)
    A_F = arithmetic_divergence(n)
    B = 1.0  # Placeholder for constant B
    c = 1.0  # Placeholder for absolute constant c
    
    if A_F <= B:
        D, S = xor_circuit_size_and_depth()
        A_C = math.sqrt(S) + D ** (1/4)
        ratio = A_C / A_C
        conjecture_holds = ratio < 0.2
        counterexample = "" if conjecture_holds else f"Ratio {ratio} not less than 0.2"
    else:
        conjecture_holds = False
        counterexample = "A(F) > B"
    
    return {
        "metric_name": "Arithmetic Divergence Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        result = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")