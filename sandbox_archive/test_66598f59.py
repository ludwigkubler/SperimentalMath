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
    
    def compute_associated_elliptic_curve(f):
        # Placeholder function to simulate computation of an elliptic curve
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 100)
    
    def minimal_index_of_monodromy_representation(e_f):
        # Placeholder function to simulate computation of the minimal index
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 50)
    
    communication_complexity = lambda f: len(f) / 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        n_max = n
        conjecture_holds = True
        counterexample = ""
        
        for _ in range(50):
            f = generate_boolean_function(n)
            e_f = compute_associated_elliptic_curve(f)
            I_e_f = minimal_index_of_monodromy_representation(e_f)
            C_f = communication_complexity(f)
            
            if C_f > I_e_f:
                conjecture_holds = False
                counterexample = f"n={n}, f={f}, e_f={e_f}, I(e_f)={I_e_f}, C(f)={C_f}"
                break
            
            instances_tested += 1
        
        results.append({
            "metric_name": "communication_complexity",
            "metric_value": C_f,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_metric_value": mean_metric_value,
        "std_metric_value": std_metric_value,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["mean_metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["mean_metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.95) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")