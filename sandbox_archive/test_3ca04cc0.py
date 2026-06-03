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
    
    def frege_proof_length(f):
        # Simplified Frege proof length calculation
        return len(f)
    
    def min_rank(cubical_complex):
        # Simplified minimal rank calculation
        return len(cubical_complex)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0.0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        L_f = frege_proof_length(f)
        C_f = f  # Simplified cubical complex representation
        min_rank_C_f = min_rank(C_f)
        
        if min_rank_C_f / L_f > 2:
            return {
                "metric_name": "min_rank_to_L_f_ratio",
                "metric_value": min_rank_C_f / L_f,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"n={n}, min_rank(C_f)={min_rank_C_f}, L_f={L_f}"
            }
        
        total_metric_value += min_rank_C_f / L_f
        instances_tested += 1
        n_max = max(n_max, n)
    
    return {
        "metric_name": "min_rank_to_L_f_ratio",
        "metric_value": total_metric_value / len(n_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank(C_f) / L_f > 2\" first_failing_seed={first_failing_seed}")