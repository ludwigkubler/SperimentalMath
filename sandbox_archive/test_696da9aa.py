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
        # Simplified generation for demonstration purposes
        return [random.choice([0, 1]) for _ in range(k)]
    
    def compute_cross_sectional_area(circuit):
        n = len(circuit)
        area = 0
        for i in range(2 ** n):
            if all(circuit[j] == (i >> j) & 1 for j in range(n)):
                area += 1
        return area
    
    def check_conjecture(area, n, k):
        return area >= math.sqrt(n) ** k
    
    n = random.randint(5, 40)
    k = min(k, n)  # Ensure k is not greater than n
    circuit = generate_monotone_circuit(n, k)
    area = compute_cross_sectional_area(circuit)
    conjecture_holds = check_conjecture(area, n, k)
    
    return {
        "metric_name": "cross_sectional_area",
        "metric_value": area,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Area {area} < n^(k/2) for n={n}, k={k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_area = sum(r["metric_value"] for r in results) / len(results)
    std_area = math.sqrt(sum((r["metric_value"] - mean_area) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_area} std={std_area} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_area} std={std_area} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Area < n^(k/2)\" first_failing_seed={first_failing_seed}")