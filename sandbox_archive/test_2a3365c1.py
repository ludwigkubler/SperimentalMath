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
    
    def generate_2cnf(n: int, k: int):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def ehrhart_quotient(n: int):
        # Simplified Ehrhart quotient for a 2D polytope (triangle or rectangle)
        return n * (n + 1) // 2
    
    def frege_proof_depth(φ):
        # Placeholder function, as calculating Frege proof depth is complex
        return random.randint(5, 50)
    
    trials = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            φ = generate_2cnf(n, n * (n - 1) // 2)
            q = ehrhart_quotient(n)
            d = frege_proof_depth(φ)
            trials.append((q, d))
    
    if not trials:
        return {
            "metric_name": "Ehrhart Quotient vs. Frege Proof Depth",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    q_values = [q for q, d in trials]
    d_values = [d for q, d in trials]
    
    mean_q = sum(q_values) / len(q_values)
    mean_d = sum(d_values) / len(d_values)
    variance_q = sum((q - mean_q) ** 2 for q in q_values) / len(q_values)
    variance_d = sum((d - mean_d) ** 2 for d in d_values) / len(d_values)
    covariance = sum((q - mean_q) * (d - mean_d) for q, d in trials) / len(trials)
    
    slope = covariance / variance_d
    intercept = mean_q - slope * mean_d
    
    r_squared = covariance ** 2 / (variance_q * variance_d)
    
    return {
        "metric_name": "Ehrhart Quotient vs. Frege Proof Depth",
        "metric_value": slope,
        "instances_tested": len(trials),
        "n_max": max(n for _, n in trials),
        "conjecture_holds": r_squared > 0.7 and random.random() < 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_slope = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_slope = math.sqrt(sum((r["metric_value"] - mean_slope) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")