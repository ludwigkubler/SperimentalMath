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
    
    def generate_affine_variety(n):
        # Generate a random affine variety over F_2 with n variables
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_minimal_local_ring_norm(V):
        # Compute the minimal local ring norm of V (simplified example)
        return sum(V) / len(V)
    
    def compute_frege_proof_length(V):
        # Simulate computing Frege proof length (simplified example)
        return len(V) * 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        V = generate_affine_variety(n)
        mrl_V = compute_minimal_local_ring_norm(V)
        f_V = compute_frege_proof_length(V)
        
        results.append({
            "n": n,
            "mrl_V": mrl_V,
            "f_V": f_V
        })
    
    if len(results) < 24:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    mrl_values = [r["mrl_V"] for r in results]
    f_values = [r["f_V"] for r in results]
    
    mean_mrl = sum(mrl_values) / len(mrl_values)
    mean_f = sum(f_values) / len(f_values)
    
    covariance = sum((mrl_values[i] - mean_mrl) * (f_values[i] - mean_f) for i in range(len(results))) / len(results)
    variance_mrl = sum((mrl_values[i] - mean_mrl)**2 for i in range(len(results))) / len(results)
    variance_f = sum((f_values[i] - mean_f)**2 for i in range(len(results))) / len(results)
    
    pearson_corr_coeff = covariance / (math.sqrt(variance_mrl) * math.sqrt(variance_f))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr_coeff,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": pearson_corr_coeff >= 0.6,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")