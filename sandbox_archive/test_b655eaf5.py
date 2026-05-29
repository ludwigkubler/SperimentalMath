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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def frege_proof_complexity(f):
    n = int(math.log2(len(f)))
    if 2**n != len(f):
        raise ValueError("Input list length must be a power of 2")
    
    # Simplified Frege proof complexity calculation
    return n

def categorical_representation(f):
    n = int(math.log2(len(f)))
    if 2**n != len(f):
        raise ValueError("Input list length must be a power of 2")
    
    monoids = set()
    for i in range(2**n):
        for j in range(2**n):
            if (f[i] and f[j]) == f[(i & j) % 2**n]:
                monoids.add((i, j))
    
    return len(monoids)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        d_f = frege_proof_complexity(f)
        D_f = d_f
        monoids = categorical_representation(f)
        
        if monoids > D_f**3:
            return {
                "metric_name": "Monoids vs Depth^3",
                "metric_value": monoids,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, Monoids={monoids}, D(f)^3={D_f**3}"
            }
        
        results.append({
            "n": n,
            "d_f": d_f,
            "D_f": D_f,
            "monoids": monoids
        })
    
    mean_metric_value = sum(result["monoids"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["monoids"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = all(result["monoids"] <= result["D_f"]**3 for result in results)
    
    return {
        "metric_name": "Monoids vs Depth^3",
        "metric_value": mean_metric_value,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = all(r["conjecture_holds"] for r in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")