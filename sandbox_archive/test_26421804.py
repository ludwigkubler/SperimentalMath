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
    
    def generate_bp(n):
        gates = []
        for _ in range(2 * n - 1):
            if random.choice([True, False]):
                gates.append((random.randint(0, n-1), random.randint(0, n-1)))
            else:
                gates.append((random.randint(0, n-1),))
        return gates
    
    def compute_rho(bp):
        m = len(bp)
        n = max(max(g) for g in bp if isinstance(g, tuple)) + 1
        rho = m / (n * math.log(n))
        return rho
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        bp = generate_bp(n)
        rho = compute_rho(bp)
        results.append(rho)
    
    mean_value = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    conjecture_holds = all(abs(rho - (len(bp) / (n * math.log(n)))) <= 3 * std_dev for rho, bp, n in zip(results, [generate_bp(random.randint(5, 40)) for _ in range(len(results))], [random.randint(5, 40)] * len(results)))
    correlation_coefficient = sum((x - mean_value) * (y - mean_value) for x, y in zip(results, [len(generate_bp(n)) / (n * math.log(n)) for n in range(5, 41)])) / (len(results) * std_dev * std_dev)
    
    return {
        "metric_name": "Correlation coefficient between ρ(P) and size of BP",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "rho_outside_bounds"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rho_outside_bounds' first_failing_seed={first_failing_seed}")