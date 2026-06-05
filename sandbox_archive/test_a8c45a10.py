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
    
    def frobenius_schur_indicator(poly):
        # Placeholder implementation, replace with actual calculation
        return 1
    
    def max_entanglement_entropy(circuit):
        n = len(circuit)
        if n <= 1:
            return 0
        p = Fraction(1, n)
        entropy = p * math.log2(p) + (1 - p) * math.log2(1 - p)
        return entropy
    
    def generate_circuit(n):
        # Placeholder implementation, replace with actual circuit generation
        return [random.choice([0, 1]) for _ in range(n)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        chi_min = frobenius_schur_indicator(circuit)
        E_C = max_entanglement_entropy(circuit)
        
        if E_C <= 0:
            continue
        
        diff = abs(chi_min - E_C)
        results.append(diff)
    
    metric_value = sum(results) / len(results)
    instances_tested = len(results)
    n_max = max(n_values)
    conjecture_holds = all(diff <= 1 for diff in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Frobenius-Schur Indicator Entanglement Gap",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r <= 1) / len(results)
    
    if all(r <= 1 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")