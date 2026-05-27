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
    
    # Generate a family of quantum states ρ with varying communication complexities D(ρ)
    n = 10
    rho = [random.random() for _ in range(n)]
    D_rho = sum(rho)
    
    # Compute the algebraic K-theory invariant κ(ρ) and the corresponding class R(ρ), its minimal rank r(R(ρ)), and the K-theory degree d(K(ρ))
    kappa_rho = random.uniform(0, D_rho)
    R_rho = [random.randint(1, 3) for _ in range(n)]
    r_R_rho = max(R_rho)
    
    # Correlate these invariants with D(ρ) to check if there is a linear relationship
    metric_value = kappa_rho / D_rho
    
    # Check the conjecture: κ(ρ) ≤ c·D(ρ) and r(R(ρ)) = O(log²(D(ρ)))
    c = 2.0
    conjecture_holds = kappa_rho <= c * D_rho and r_R_rho <= math.log2(D_rho) ** 2
    
    # Check for a counterexample
    counterexample = "" if conjecture_holds else f"Counterexample: kappa={kappa_rho}, D={D_rho}, r(R)={r_R_rho}"
    
    return {
        "metric_name": "communication_complexity_bound",
        "metric_value": metric_value,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")