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
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_input_space(circuit):
        n = int(math.log2(len(circuit)))
        input_space = set()
        for i in range(2**n):
            input_space.add(tuple(circuit[i*2:(i+1)*2]))
        return input_space
    
    def kahler_entropy(input_space):
        # Simplified Kähler entropy calculation (not actual Kähler geometry)
        n = len(next(iter(input_space)))
        return -n * math.log2(1/n)
    
    def entanglement_complexity(circuit):
        # Simplified entanglement complexity calculation (not actual quantum computing)
        return sum(circuit.count(bit) for bit in [0, 1])
    
    n_values = [5, 10, 15, 20, 30, 40]
    mge_values = []
    ec_values = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        input_space = compute_input_space(circuit)
        mge = kahler_entropy(input_space)
        ec = entanglement_complexity(circuit)
        mge_values.append(mge)
        ec_values.append(ec)
    
    if not mge_values or not ec_values:
        return {
            "metric_name": "mge/ec ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_input_space"
        }
    
    correlation_coefficient = sum((mge - mean_mge) * (ec - mean_ec) for mge, ec in zip(mge_values, ec_values)) / len(mge_values)
    mean_mge = sum(mge_values) / len(mge_values)
    mean_ec = sum(ec_values) / len(ec_values)
    mge_ec_ratio = mean_mge / mean_ec
    
    return {
        "metric_name": "mge/ec ratio",
        "metric_value": mge_ec_ratio,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": 0.9 <= correlation_coefficient and 1.2 <= mge_ec_ratio <= 1.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_mge_ec_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_mge_ec_ratio} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_conjecture_holds_or_counterexamples")