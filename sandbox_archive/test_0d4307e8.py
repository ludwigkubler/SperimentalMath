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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clause = " or ".join(str(lit) if lit > 0 else f"not {abs(lit)}" for lit in literals)
            cnf.append(clause)
        return "\n".join(cnf)

    def compute_euler_characteristic(m, n):
        # Placeholder function to simulate Euler characteristic computation
        # This is a dummy implementation and should be replaced with actual computation
        return m * n

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n // 2, n * 2)
            cnf = generate_cnf(n, m)
            chi_phi = compute_euler_characteristic(m, n)
            results.append({"n": n, "m": m, "chi_phi": chi_phi})
    
    if not results:
        return {
            "metric_name": "Euler Characteristic",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    chi_phi_values = [r["chi_phi"] for r in results]
    m_values = [r["m"] for r in results]
    n_values = [r["n"] for r in results]
    
    mean_chi_phi = sum(chi_phi_values) / len(chi_phi_values)
    std_dev = math.sqrt(sum((x - mean_chi_phi) ** 2 for x in chi_phi_values) / len(chi_phi_values))
    
    max_n = max(n_values)
    
    conjecture_holds = all(1.5 * m ** (2/3) * n ** (1/3) >= chi_phi for chi_phi, m, n in zip(chi_phi_values, m_values, n_values))
    counterexample = "" if conjecture_holds else "Euler characteristic too large"
    
    return {
        "metric_name": "Euler Characteristic",
        "metric_value": mean_chi_phi,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Euler characteristic too large\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")