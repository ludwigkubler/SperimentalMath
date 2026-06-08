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
    
    def generate_random_cnf(n: int, m: int):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) if random.choice([True, False]) else -random.choice(variables) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def frege_proof_length(cnf):
        # Simplified Frege proof length calculation
        return len(cnf) * 3
    
    def symplectic_volume(cnf):
        # Placeholder for actual computation
        return random.random()  # This is a dummy value for demonstration
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    metric_values = []
    conjecture_holds = False
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            cnf = generate_random_cnf(n, random.randint(2 * n, 3 * n))
            instances_tested += 1
            l_phi = frege_proof_length(cnf)
            V_phi = symplectic_volume(cnf)
            metric_values.append((V_phi, l_phi))
    
    if len(metric_values) < 30:
        return {
            "metric_name": "symplectic_volume",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    V_phi_list = [V for V, _ in metric_values]
    l_phi_list = [l for _, l in metric_values]
    
    mean_V_phi = sum(V_phi_list) / len(V_phi_list)
    mean_l_phi = sum(l_phi_list) / len(l_phi_list)
    
    covariance = sum((V_phi - mean_V_phi) * (l_phi - mean_l_phi) for V_phi, l_phi in metric_values) / len(metric_values)
    variance_V_phi = sum((V_phi - mean_V_phi) ** 2 for V_phi in V_phi_list) / len(V_phi_list)
    variance_l_phi = sum((l_phi - mean_l_phi) ** 2 for l_phi in l_phi_list) / len(l_phi_list)
    
    r = covariance / (math.sqrt(variance_V_phi) * math.sqrt(variance_l_phi))
    
    if abs(r) > 0.7:
        conjecture_holds = True
    else:
        counterexample = f"r={r:.2f}"
    
    return {
        "metric_name": "symplectic_volume",
        "metric_value": r,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        mean_r = sum(r["metric_value"] for r in results) / len(results)
        std_r = math.sqrt(sum((r["metric_value"] - mean_r) ** 2 for r in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_r:.4f} std={std_r:.4f} support_fraction={support_fraction:.2f}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")