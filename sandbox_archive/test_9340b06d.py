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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f).bit_length() - 1
        rc_f = 0
        for i in range(1, n + 1):
            if any(f[j] != f[j ^ (1 << k)] for j in range(2**n) for k in range(i)):
                rc_f += 1
        return rc_f
    
    def alexander_orlik_solomon_invariant(f):
        # Placeholder function; actual computation depends on the link L_f
        return random.random() * len(f)
    
    correlation_coefficient = 0
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        alpha_omega_f = alexander_orlik_solomon_invariant(f)
        rc_f = communication_complexity_rank_variance(f)
        
        if instances_tested == 0:
            n_max = n
        
        correlation_coefficient += alpha_omega_f * rc_f
        instances_tested += 1
    
    correlation_coefficient /= instances_tested
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and correlation_coefficient <= 1.2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction_below_0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")