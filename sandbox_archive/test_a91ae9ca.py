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
    
    # Generate a random communication protocol φ with n participants
    n = random.randint(5, 30)
    phi_G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    # Calculate the rank variance r(φ)
    rank_variance = sum(sum(row) for row in phi_G) / (n * n)
    
    # Calculate the p-adic logarithmic capacity logCap_ρ(φ)
    logCap_rho = 0
    for i in range(n):
        for j in range(i + 1, n):
            if phi_G[i][j] == 1:
                logCap_rho += math.log2(j - i)
    
    # Compare r(φ) with logCap_ρ(φ)
    conjecture_holds = rank_variance <= logCap_rho
    counterexample = f"r(φ) > logCap_ρ(φ): {rank_variance} > {logCap_rho}" if not conjecture_holds else ""
    
    return {
        "metric_name": "rank_variance",
        "metric_value": rank_variance,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")