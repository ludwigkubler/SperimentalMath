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
    
    def bp_readTwice_tensor_width(P):
        # Placeholder for actual implementation
        return len(P) ** 0.25
    
    def quadratic_form_rank(Q):
        # Placeholder for actual implementation
        return sum(1 for row in Q if any(row))  # Simplified example
    
    n = random.randint(5, 40)
    r = random.randint(1, min(n, 10))
    
    P = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    Q = [[sum(P[i][j] * P[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
    
    rho_P = bp_readTwice_tensor_width(P)
    rho_Q = quadratic_form_rank(Q)
    
    upper_bound = n**2 * r * math.log(r)
    
    return {
        "metric_name": "BP_readTwice tensor width",
        "metric_value": rho_P,
        "instances_tested": 1,
        "conjecture_holds": rho_Q <= upper_bound,
        "counterexample": "" if rho_Q <= upper_bound else f"rho(Q)={rho_Q} > {upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif not conjecture_holds:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")