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
    
    def generate_circuit(n):
        if n == 1:
            return ['0', '1']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [f'AND({l}, {r})' for l in left for r in right] + \
                   [f'OR({l}, {r})' for l in left for r in right]
    
    def monotone_complexity(circuit):
        if isinstance(circuit, str) and circuit[0] == '0' or circuit[0] == '1':
            return 1
        elif circuit.startswith('AND'):
            return 1 + max(monotone_complexity(circuit[4:circuit.index(')')]), monotone_complexity(circuit[circuit.index(',')+2:]))
        elif circuit.startswith('OR'):
            return 1 + max(monotone_complexity(circuit[3:circuit.index(')')]), monotone_complexity(circuit[circuit.index(',')+2:]))
    
    def kac_moody_rank(circuit):
        if isinstance(circuit, str) and circuit[0] == '0' or circuit[0] == '1':
            return 1
        elif circuit.startswith('AND'):
            left = kac_moody_rank(circuit[4:circuit.index(')')])
            right = kac_moody_rank(circuit[circuit.index(',')+2:])
            return max(left, right)
        elif circuit.startswith('OR'):
            left = kac_moody_rank(circuit[3:circuit.index(')')])
            right = kac_moody_rank(circuit[circuit.index(',')+2:])
            return max(left, right)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n)
            mu_C = monotone_complexity(circuit)
            r_A_C = kac_moody_rank(circuit)
            metrics.append((mu_C, r_A_C))
    
    if len(metrics) < 30:
        return {
            "metric_name": "r(A_C)",
            "metric_value": None,
            "instances_tested": len(metrics),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mu = [m[0] for m in metrics]
    r_A_C = [m[1] for m in metrics]
    
    mean_mu = sum(mu) / len(mu)
    mean_r_A_C = sum(r_A_C) / len(r_A_C)
    
    ssr = sum((r - mean_r_A_C) ** 2 for r in r_A_C)
    sst = sum((m - mean_mu) ** 2 for m in mu)
    
    if sst == 0:
        return {
            "metric_name": "r(A_C)",
            "metric_value": None,
            "instances_tested": len(metrics),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "constant_metric"
        }
    
    r_squared = ssr / sst
    p_value = 2 * (1 - math.erf(abs(r_squared) * math.sqrt(len(mu) - 2) / math.sqrt(2)))
    
    return {
        "metric_name": "r(A_C)",
        "metric_value": r_squared,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": r_squared >= 0.9 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r_squared = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")