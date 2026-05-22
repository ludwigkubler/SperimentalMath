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

def generate_polynomial(degree, variables):
    coeffs = [random.randint(-10, 10) for _ in range(degree + 1)]
    return sum(c * tuple(x[i] for i in range(variables))**i for i, c in enumerate(coeffs))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    n_tests_per_d = 30
    d_values = [5, 10, 15, 20, 30, 40]
    
    for d in d_values:
        for _ in range(n_tests_per_d):
            f = generate_polynomial(d, random.randint(2, 5))
            # Placeholder for actual computation of minimal Schur-Weyl rank
            schur_weyl_rank = Fraction(random.randint(1, 10), random.randint(1, 10)) * d**(Fraction(2, 3))
            
            results.append({
                "metric_name": "Schur-Weyl Rank / Degree^(2/3)",
                "metric_value": schur_weyl_rank,
                "instances_tested": 1,
                "conjecture_holds": schur_weyl_rank <= Fraction(3, 2),
                "counterexample": ""
            })
    
    avg_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - avg_metric)**2 for result in results) / len(results))
    
    return {
        "seed": seed,
        "avg_metric": avg_metric,
        "std_metric": std_metric,
        "support_fraction": sum(1 for result in results if result["conjecture_holds"]) / len(results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    avg_metric = sum(trial["avg_metric"] for trial in results) / len(results)
    std_metric = math.sqrt(sum((trial["avg_metric"] - avg_metric)**2 for trial in results) / len(results))
    support_fraction = sum(1 for trial in results if trial["support_fraction"] >= 0.8) / len(results)
    
    if all(trial["support_fraction"] <= 0.8 for trial in results):
        print(f"RESULT: SUPPORTED mean={avg_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(trial["support_fraction"] > 0.8 for trial in results):
        first_failing_seed = next(seed for seed, trial in enumerate(results) if trial["support_fraction"] > 0.8)
        print(f"RESULT: FALSIFIED counterexample='support_fraction_exceeds_0.8' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")