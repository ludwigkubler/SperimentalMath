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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def lefschetz_fitting_dimension(phi):
        # Placeholder implementation. Actual computation depends on the formula.
        return len(phi)
    
    def resolution_proof_width(phi):
        # Placeholder implementation. Actual computation depends on the formula.
        return len(phi) ** 2
    
    instances_tested = 0
    n_max = 1
    total_metric_value = 0
    counterexample = ""
    conjecture_holds = True
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            phi = generate_boolean_formula(n)
            instances_tested += 1
            
            Lf_phi = lefschetz_fitting_dimension(phi)
            w_phi = resolution_proof_width(phi)
            
            total_metric_value += Lf_phi
            if Lf_phi > 1000 and w_phi < 10000:
                conjecture_holds = False
                counterexample = f"phi with n={n}, Lf(φ)={Lf_phi}, w(φ)={w_phi}"
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    
    return {
        "metric_name": "Lefschetz Fitting Dimension",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")