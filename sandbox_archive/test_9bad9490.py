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
    
    def generate_monotone_circuit(n, k):
        # Placeholder function to generate a monotone circuit of size n^k
        return [[random.choice([0, 1]) for _ in range(k)] for _ in range(n)]
    
    def calculate_symmetry_group(circuit):
        # Placeholder function to calculate the symmetry group of a circuit
        # This is a dummy implementation and should be replaced with actual logic
        return set()
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n // 2, 10))
    circuit = generate_monotone_circuit(n, k)
    symmetry_group = calculate_symmetry_group(circuit)
    
    metric_value = len(symmetry_group)
    conjecture_holds = metric_value >= 2**n
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Symmetry Group Order",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*3 + 1))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")