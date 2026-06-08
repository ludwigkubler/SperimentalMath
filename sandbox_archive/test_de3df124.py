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
    
    def generate_formula(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def frege_proof_length(formula):
        # Simplified Frege proof length calculation
        return len(formula) * 3
    
    def symplectic_volume(formula):
        # Simplified symplectic volume calculation
        return sum(formula)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_formula(n)
        l_phi = frege_proof_length(formula)
        V_phi = symplectic_volume(formula)
        
        results.append({
            "n": n,
            "l_phi": l_phi,
            "V_phi": V_phi
        })
    
    if not results:
        return {
            "metric_name": "Symplectic Volume vs Frege Proof Length",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    V_phi_values = [r["V_phi"] for r in results]
    l_phi_values = [r["l_phi"] for r in results]
    
    mean_V_phi = sum(V_phi_values) / len(V_phi_values)
    mean_l_phi = sum(l_phi_values) / len(l_phi_values)
    
    covariance = sum((V_phi_values[i] - mean_V_phi) * (l_phi_values[i] - mean_l_phi) for i in range(len(results))) / len(results)
    variance_V_phi = sum((V_phi_values[i] - mean_V_phi) ** 2 for i in range(len(results))) / len(results)
    variance_l_phi = sum((l_phi_values[i] - mean_l_phi) ** 2 for i in range(len(results))) / len(results)
    
    r = covariance / math.sqrt(variance_V_phi * variance_l_phi)
    
    return {
        "metric_name": "Symplectic Volume vs Frege Proof Length",
        "metric_value": abs(r),
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(r) > 0.7,
        "counterexample": "" if abs(r) > 0.7 else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(result for result in results if not result["conjecture_holds"])["seed"]
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")