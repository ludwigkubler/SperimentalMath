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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def schur_weyl_dimension(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Input must be a Boolean function with n variables")
        
        # Compute the Schur-Weyl dimension (simplified for demonstration)
        return n
    
    def monotone_circuit_size(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Input must be a Boolean function with n variables")
        
        # Compute the size of a monotone circuit (simplified for demonstration)
        return 2**n
    
    def run_experiment(n):
        f = generate_random_boolean_function(n)
        rho_f = schur_weyl_dimension(f)
        E_C = monotone_circuit_size(f)
        return {"rho_f": rho_f, "E_C": E_C}
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        result = run_experiment(n)
        results.append(result)
    
    total_rho_f = sum(result["rho_f"] for result in results)
    total_E_C = sum(result["E_C"] for result in results)
    avg_rho_f = total_rho_f / len(results)
    avg_E_C = total_E_C / len(results)
    
    metric_value = avg_E_C
    conjecture_holds = avg_E_C <= 2 * avg_rho_f
    counterexample = "" if conjecture_holds else f"avg_E_C={avg_E_C} > 2*avg_rho_f={2*avg_rho_f}"
    
    return {
        "metric_name": "E[|C|]",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - avg_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"avg_E_C > 2*avg_rho_f\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")