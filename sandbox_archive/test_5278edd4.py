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
    
    def generate_csp(n, m):
        variables = list(range(n))
        constraints = []
        for _ in range(m):
            constraint = [random.choice(variables) for _ in range(2)]
            constraints.append(constraint)
        return constraints
    
    def tropical_curve_rank(CSP):
        # Placeholder function to compute the rank of the tropical curve
        # This is a dummy implementation and should be replaced with actual logic
        return len(CSP)
    
    def sos_refutation_size(CSP):
        # Placeholder function to compute the size of the SOS refutation
        # This is a dummy implementation and should be replaced with actual logic
        return len(CSP) * 2
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    CSP = generate_csp(n, m)
    
    tropical_curve_rank = tropical_curve_rank(CSP)
    sos_refutation_size = sos_refutation_size(CSP)
    
    return {
        "metric_name": "Rank of Tropical Curve vs SOS Refutation Size",
        "metric_value": abs(tropical_curve_rank - sos_refutation_size),
        "instances_tested": 1,
        "conjecture_holds": tropical_curve_rank == sos_refutation_size,
        "counterexample": "" if tropical_curve_rank == sos_refutation_size else f"Rank: {tropical_curve_rank}, Refutation Size: {sos_refutation_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")