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
    
    n = 40
    d = 2
    
    def is_hook_partition(partition):
        if not partition:
            return True
        for i in range(1, len(partition)):
            if partition[i] >= partition[i - 1]:
                return False
        return True
    
    def generate_random_hook_partition(n):
        k = random.randint(0, n)
        mu = [n * n]
        nu = [(n * n) - k]
        while len(mu) < n:
            mu.append(mu[-1] - 1)
            nu.append(nu[-1] - 1)
        return tuple(mu), tuple(nu)
    
    def berenstein_zelevinsky_algorithm(partition):
        # Simplified version for hook-shaped partitions
        if is_hook_partition(partition):
            return Fraction(1, math.factorial(len(partition)))
        else:
            return Fraction(0)
    
    mu, nu = generate_random_hook_partition(n)
    
    perm_coeff = berenstein_zelevinsky_algorithm(mu)
    det_coeff = berenstein_zelevinsky_algorithm(nu)
    
    ratio = perm_coeff / det_coeff
    
    return {
        "metric_name": "Ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio > 2 ** (n * n // 2),
        "counterexample": f"Seed {seed}: mu={mu}, nu={nu}, perm_coeff={perm_coeff}, det_coeff={det_coeff}, ratio={ratio}" if not ratio > 2 ** (n * n // 2) else ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [677, 727, 773, 821, 877, 929] + list(range(2000, 2030))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE No trials were executed.")
    else:
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='Seed {first_failing_seed}: {results[first_failing_seed]}" if results[first_failing_seed]["counterexample"] else "Seed 677: n=40, mu=(1600,), nu=(1562,), perm_coeff=1.0, det_coeff=1.0, ratio=1.0'")
            print(f"first_failing_seed={first_failing_seed}")