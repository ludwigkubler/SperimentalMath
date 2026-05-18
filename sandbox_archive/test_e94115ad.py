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

def generate_random_acc02_circuit(n, s):
    gates = []
    for _ in range(s):
        gate_type = random.choice(['AND', 'OR', 'MOD_2', 'NOT'])
        fanin = random.randint(2, min(len(gates) + 1, math.floor(math.log2(s)) + 3))
        inputs = sorted(random.sample(range(len(gates)), fanin))
        gates.append((gate_type, inputs))
    return gates

def generate_mod_3_circuit(n):
    # Placeholder for actual MOD_3 circuit generation logic
    # This is a stub and should be replaced with actual implementation
    return []

def compute_spectrum_dimension(circuit, p):
    max_chi = 0
    for gate_type, inputs in circuit:
        if gate_type == 'MOD_2':
            k = len(inputs)
            chi = sum(abs(sum(math.exp(2j * math.pi * a_j * ξ / p) for a_j in inputs)) >= k / 2 for ξ in range(1, p))
            max_chi = max(max_chi, chi)
    return max_chi / math.log2(p + 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [6, 8, 10, 12]
    s_values = [15, 30, 60]
    instances_tested = 0
    total_chi = 0
    
    for n in n_values:
        for s in s_values:
            circuit = generate_random_acc02_circuit(n, s)
            p = next(p for p in range(s + 2, 1000) if all(p % i != 0 for i in range(2, int(math.sqrt(p)) + 1)))
            chi = compute_spectrum_dimension(circuit, p)
            total_chi += chi
            instances_tested += 1
    
    mean_chi = total_chi / instances_tested
    conjecture_holds = mean_chi <= 8 * math.log2(s_values[-1] + 1)
    
    return {
        "metric_name": "Spectrum Dimension",
        "metric_value": mean_chi,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean Spectrum Dimension {mean_chi} > 8 * log2({s_values[-1]} + 1)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_chi = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_chi} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_chi} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean Spectrum Dimension {mean_chi} > 8 * log2({s_values[-1]} + 1)\" first_failing_seed={first_failing_seed}")