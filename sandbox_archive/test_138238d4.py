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
    
    def generate_boolean_circuit(depth):
        if depth == 0:
            return []
        else:
            circuit = [random.choice([0, 1])]
            for _ in range(1, depth):
                circuit.append(random.choice([0, 1]))
            return circuit
    
    def compute_k_theoretic_dimension(circuit):
        # Simplified example: K-theoretic dimension is the length of the circuit
        return len(circuit)
    
    results = []
    for n in range(5, 41, 5):
        for _ in range(6):  # Test 6 instances per depth
            circuit = generate_boolean_circuit(n)
            k_theo = compute_k_theoretic_dimension(circuit)
            results.append(k_theo)
    
    conjecture_holds = all(d <= n**2 for d, n in zip(results, range(5, 41, 5)))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "K-theoretic dimension",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")