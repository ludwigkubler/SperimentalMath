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
        # Placeholder for generating a monotone circuit computing k-CLIQUE
        return [[random.choice([0, 1]) for _ in range(k)] for _ in range(n)]
    
    def compute_cross_sectional_area(circuit):
        n = len(circuit)
        area = 0
        for i in range(2**n):
            support_hyperplane = [i >> j & 1 for j in range(n)]
            count = sum(1 for row in circuit if all(row[j] == support_hyperplane[j] for j in range(k)))
            area = max(area, count)
        return area
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_monotone_circuit(n, k)
        area = compute_cross_sectional_area(circuit)
        expected_area = math.ceil(n ** (k / 2))
        if area < expected_area:
            return {
                "metric_name": "cross_sectional_area",
                "metric_value": area,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, circuit={circuit}, computed_area={area}, expected_area={expected_area}"
            }
    
    return {
        "metric_name": "cross_sectional_area",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= math.ceil(n_values[-1] ** (k / 2))) / len(results)
    
    if all(r >= math.ceil(n_values[-1] ** (k / 2)) for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if r < math.ceil(n_values[-1] ** (k / 2)))]
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")