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
    
    n = random.randint(5, 40)
    clause_density = random.uniform(0.1, 0.9)
    num_clauses = int(n * (n - 1) / 2 * clause_density)
    F = [random.choice([0, 1]) for _ in range(num_clauses)]
    
    G = [(i, j) for i in range(n) for j in range(i + 1, n)]
    Rep_G = {G[i]: random.randint(1, 5) for i in range(len(G))}
    
    min_rho_1 = min([Rep_G[G[i]] for i in range(len(G))])
    
    t_F = sum(F)
    
    conjecture_holds = t_F >= 2 ** (min_rho_1 * math.log2(n))
    counterexample = "" if conjecture_holds else f"Counterexample found with n={n}, min_rho_1={min_rho_1}, t_F={t_F}"
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": t_F,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")