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

def generate_ac0_circuit(n):
    circuit = [random.choice([0, 1]) for _ in range(n)]
    return circuit

def q_series(circuit):
    n = len(circuit)
    series = []
    for i in range(1, n + 1):
        term = (math.exp(-i) * sum(circuit[j] for j in range(i, n, i))) / math.factorial(i)
        if term == 0:
            break
        series.append(term)
    return series

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_ac0_circuit(n)
    
    series = q_series(circuit)
    if not series:
        return {
            "metric_name": "q-series_convergence",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "empty_series"
        }
    
    convergence_threshold = 0.01
    if abs(sum(series)) < convergence_threshold:
        return {
            "metric_name": "q-series_convergence",
            "metric_value": sum(series),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "does_not_converge"
        }
    
    return {
        "metric_name": "q-series_convergence",
        "metric_value": sum(series),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")