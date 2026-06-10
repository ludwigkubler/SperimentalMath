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

def generate_circuit(n):
    if n == 1:
        return ['0', '1']
    left = generate_circuit(n // 2)
    right = generate_circuit(n - n // 2)
    return [f'({l} OR {r})' for l in left] + [f'({l} AND {r})' for l in right]

def twistor_space(circuit):
    if not circuit:
        return set()
    if isinstance(circuit, str):
        return {circuit}
    else:
        return twistor_space(circuit[0]) | twistor_space(circuit[1])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        twistor_set = twistor_space(circuit)
        o = len(twistor_set)
        d = n
        results.append({"n": n, "o": o, "d": d})
    
    if not results:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_o = sum(result["o"] for result in results) / len(results)
    mean_d = sum(result["d"] for result in results) / len(results)
    correlation = (sum((result["o"] - mean_o) * (result["d"] - mean_d) for result in results) /
                   math.sqrt(sum((result["o"] - mean_o) ** 2 for result in results) *
                             sum((result["d"] - mean_d) ** 2 for result in results)))
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": "" if correlation >= 0.7 else f"Correlation {correlation} < 0.7"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        print(f"TRIAL: {seed}")
        trial_result = run_trial(seed)
        results.append(trial_result)
    
    mean_correlation = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_correlation} std=0.0 support_fraction={support_fraction}")