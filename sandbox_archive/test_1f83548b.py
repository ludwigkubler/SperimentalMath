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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def schubert_polynomial_representation(n):
        # Placeholder for actual Schubert polynomial representation logic
        return 1 + n  # Simplified example
    
    def communication_complexity_rank(n):
        # Placeholder for actual communication complexity rank logic
        return n  # Simplified example
    
    min_monomials = float('inf')
    k_values = [5, 10, 15, 20, 30, 40]
    
    for k in k_values:
        n = random.randint(5, 40)
        rank = communication_complexity_rank(n)
        monomials = schubert_polynomial_representation(n)
        
        if monomials < min_monomials:
            min_monomials = monomials
    
    metric_value = min_monomials
    instances_tested = len(k_values)
    n_max = max(40, random.randint(5, 40))
    conjecture_holds = False
    counterexample = ""
    
    if instances_tested >= 30:
        ratio = Fraction(min_monomials, k**2 * math.log(n))
        if abs(ratio - 1) <= Fraction(3, 100):
            conjecture_holds = True
    
    return {
        "metric_name": "min_monomials",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")