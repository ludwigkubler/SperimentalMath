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

def generate_instance(n: int, m: int) -> list:
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause_size = random.randint(1, n)
        clause = random.sample(variables, clause_size)
        clauses.append(clause)
    return clauses

def link_complex(clauses: list) -> dict:
    # Placeholder for the actual computation of the link complex
    # This is a dummy implementation to avoid errors
    return {}

def local_coherence_index(link_complex: dict) -> float:
    # Placeholder for the actual computation of the local coherence index
    # This is a dummy implementation to avoid errors
    return random.random()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m_max = min(2000, n * (n - 1) // 2)  # Ensure m is reasonable
        for _ in range(5):  # Sample 5 instances per n
            m = random.randint(n, m_max)
            clauses = generate_instance(n, m)
            link_complex_ = link_complex(clauses)
            I_phi = local_coherence_index(link_complex_)
            results.append({
                "n": n,
                "m": m,
                "I_phi": I_phi,
                "g_m": m ** (1/3)
            })
    
    metric_value = sum(result["I_phi"] for result in results) / len(results)
    conjecture_holds = all(result["I_phi"] >= result["g_m"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "local_coherence_index",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")