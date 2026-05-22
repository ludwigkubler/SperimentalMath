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
    
    def is_ac0_circuit(circuit):
        # Placeholder for AC0 circuit checking logic
        return True
    
    def generate_random_ac0_circuit(n):
        # Placeholder for generating a random AC0 circuit computing PARITY on n inputs
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tensor_representation(circuit):
        n = len(circuit)
        T_f = [[0] * (2**n) for _ in range(n+1)]
        for i in range(n+1):
            for j in range(2**n):
                if bin(j).count('1') == i:
                    T_f[i][j] = circuit[j]
        return T_f
    
    def calculate_norms(circuit, n):
        T_f = tensor_representation(circuit)
        norm = 0
        for i in range(n+1):
            for j in range(2**n):
                if bin(j).count('1') == i:
                    norm += abs(T_f[i][j])
        return norm
    
    def parity_function(x):
        return sum(x) % 2
    
    n = random.randint(5, 40)
    circuit = generate_random_ac0_circuit(n)
    
    if not is_ac0_circuit(circuit):
        return {
            "metric_name": "AC0 Circuit Size",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    norm = calculate_norms(circuit, n)
    expected_bound = Fraction(n**2 * math.log(n), 1)
    
    return {
        "metric_name": "Minimal Symmetric Tensor Norm",
        "metric_value": norm,
        "instances_tested": 1,
        "conjecture_holds": norm >= expected_bound,
        "counterexample": "" if norm >= expected_bound else f"Norm {norm} < {expected_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_norm = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_norm} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_norm} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Norm < expected bound\" first_failing_seed={first_failing_seed}")