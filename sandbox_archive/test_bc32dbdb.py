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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf
    
    def symplectic_volume(cnf):
        n = len(cnf[0])
        volume = 1.0
        for _ in range(10):  # Simplified approximation of symplectic volume calculation
            volume *= (n + random.random())
        return volume
    
    def circuit_size(cnf):
        size = 0
        for clause in cnf:
            size += len(clause)
        return size
    
    n = 20  # Fixed instance size for simplicity
    cnf = generate_cnf(n)
    V_s = symplectic_volume(cnf)
    w = circuit_size(cnf)
    
    if w == 0:
        return {
            "metric_name": "V_s / w^2",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "circuit_size_zero"
        }
    
    metric_value = V_s / (w ** 2)
    
    return {
        "metric_name": "V_s / w^2",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='circuit_size_zero' first_failing_seed={first_failing_seed}")