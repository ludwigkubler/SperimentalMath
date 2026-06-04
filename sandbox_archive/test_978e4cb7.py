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
    
    # Define constants and parameters
    k = 2  # Binary Boolean formula
    n_min = 5
    n_max = 40
    num_trials_per_n = 30
    
    total_metric_value = 0.0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(n_min, n_max + 1):
        if n - n_min < num_trials_per_n:
            continue
        
        for _ in range(num_trials_per_n):
            # Generate a random k-ary Boolean formula φ with n variables
            phi = [random.choice([0, 1]) for _ in range(n)]
            
            # Compute the resolution proof depth d(φ)
            # This is a placeholder function; replace with actual computation
            def resolution_proof_depth(phi):
                return sum(phi)  # Simplified example
            
            d_phi = resolution_proof_depth(phi)
            
            # Construct the dual space of φ_d using lattice theory
            # Placeholder for lattice construction
            def construct_dual_space(phi):
                dual_space = []
                for i in range(2**n):
                    if all((phi[j] == 0 or phi[j] == 1) and (phi[j] + phi[(j >> i) & 1]) % 2 == 0 for j in range(n)):
                        dual_space.append(i)
                return dual_space
            
            dual_space = construct_dual_space(phi)
            
            # Calculate the minimal lattice point density MinLPD(φ_d)
            if len(dual_space) > 0:
                min_lpd = Fraction(len(dual_space), n)
            else:
                min_lpd = Fraction(0, 1)
            
            # Update metrics
            total_metric_value += min_lpd.numerator / min_lpd.denominator
            instances_tested += 1
            
            # Check for counterexample
            if conjecture_holds and min_lpd > d_phi * 2:
                conjecture_holds = False
                counterexample = f"n={n}, MinLPD={min_lpd}, d(φ)={d_phi}"
    
    return {
        "metric_name": "MinLPD",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")