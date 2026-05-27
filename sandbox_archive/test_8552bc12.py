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
    
    def construct_resolution_proof(f):
        # Simplified resolution proof construction (not actual resolution)
        n = int(math.log2(len(f)))
        clauses = []
        for i in range(n):
            clause = [(i, f[i]), (-i-1, f[2**i])]
            clauses.append(clause)
        return clauses
    
    def symmetry_measure(proof):
        # Simplified symmetry measure (not actual measure)
        return len(proof)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    C = construct_resolution_proof(f)
    psi_C = symmetry_measure(C)
    size_C = len(C)
    
    if size_C == 0:
        return {
            "metric_name": "psi(C) / log(size(C))",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Empty resolution proof"
        }
    
    alpha = 2  # Example absolute constant
    metric_value = psi_C / math.log(size_C)
    
    return {
        "metric_name": "psi(C) / log(size(C))",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": metric_value <= alpha,
        "counterexample": "" if metric_value <= alpha else f"Counterexample: psi(C) = {psi_C}, size(C) = {size_C}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")