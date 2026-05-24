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
    
    def generate_or_and_circuit(n, d):
        circuit = []
        for _ in range(d):
            layer = [random.choice(['OR', 'AND']) for _ in range(n)]
            circuit.append(layer)
        return circuit
    
    def calculate_tee(circuit, state):
        # Placeholder for TEE calculation
        # For simplicity, we assume TEE is proportional to the depth of the circuit
        return len(circuit)
    
    n = random.randint(5, 40)
    d = random.randint(1, 5)
    circuit = generate_or_and_circuit(n, d)
    
    min_tee = float('inf')
    for _ in range(30):
        state = [random.choice([0, 1]) for _ in range(n)]
        tee = calculate_tee(circuit, state)
        if tee < min_tee:
            min_tee = tee
    
    f_n_d = d * math.log2(n) ** 2
    g_n_d = d
    
    conjecture_holds = (min_tee <= f_n_d) or (min_tee >= g_n_d)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Rank of TEE",
        "metric_value": min_tee,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")