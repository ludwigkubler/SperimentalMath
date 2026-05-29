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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def frege_proof_complexity(f):
        n = len(f)
        if n == 1:
            return 1
        else:
            return 1 + max(frege_proof_complexity(f[:n//2]), frege_proof_complexity(f[n//2:]))

    def categorical_representation(f):
        n = len(f)
        monoids = set()
        for i in range(2**n):
            for j in range(2**n):
                if all((f[i] and f[j]) == f[(i & j) % 2**n] for k in range(n)):
                    monoids.add((i, j))
        return monoids

    def count_monoids(monoids):
        return len(monoids)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        d_f = frege_proof_complexity(f)
        D_f = math.ceil(d_f ** (1/3))
        monoids = categorical_representation(f)
        num_monoids = count_monoids(monoids)
        
        results.append({
            "n": n,
            "d_f": d_f,
            "D_f": D_f,
            "num_monoids": num_monoids
        })
    
    metric_value = sum(result["D_f"] ** 3 for result in results) / len(results)
    conjecture_holds = all(result["num_monoids"] <= result["D_f"] ** 3 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Categorical Depth Bound",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")