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
    
    def compute_additive_energy(cnf):
        n = len(cnf[0])
        energy = 0
        for a in range(2**n):
            for b in range(a+1, 2**n):
                if sum([abs(int(x) - int(y)) for x, y in zip(bin(a)[2:].zfill(n), bin(b)[2:].zfill(n))]) == n:
                    energy += 1
        return energy
    
    def compute_communication_complexity(cnf):
        # Simple deterministic protocol: each variable is queried once
        return len(cnf[0])
    
    def generate_random_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
            cnf.append(clause)
        return cnf
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            cnf = generate_random_cnf(n, random.randint(1, n))
            energy = compute_additive_energy(cnf)
            C = compute_communication_complexity(cnf)
            if C == 0:  # Avoid division by zero
                continue
            results.append({
                "n": n,
                "energy": energy,
                "C": C,
                "log_n": math.log(n, 2),
                "metric_value": energy * C * math.log(n, 2)
            })
    
    if not results:
        return {
            "metric_name": "additive_energy",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_instances_generated"
        }
    
    metric_values = [r["metric_value"] for r in results]
    instances_tested = len(results)
    conjecture_holds = all(v <= 2**n / (C * math.log(n)) for n, C, v in zip([r["n"] for r in results], [r["C"] for r in results], metric_values))
    
    return {
        "metric_name": "additive_energy",
        "metric_value": sum(metric_values) / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "energy * C * log n > 2^n"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"energy * C * log n > 2^n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_results")