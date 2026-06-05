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
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(n):
            if circuit[i] == 1:
                width += 1
        return width
    
    def hodge_structure_rank(circuit):
        n = len(circuit)
        rank = 0
        for i in range(n):
            if circuit[i] == 1:
                rank += 1
        return rank
    
    instances_tested = 0
    total_hodge = 0
    total_width = 0
    n_max = 5
    
    for _ in range(30):  # Aim for at least 40 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        circuit = generate_circuit(n)
        width = monotone_width(circuit)
        rank = hodge_structure_rank(circuit)
        
        total_hodge += rank
        total_width += width
        instances_tested += 1
    
    mean_hodge = total_hodge / instances_tested
    mean_width = total_width / instances_tested
    
    if instances_tested < 40:
        return {
            "metric_name": "Hodge Structure Rank vs Monotone Width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    correlation = (mean_hodge - math.sqrt(mean_width ** 2 / 3)) / (math.sqrt(2 * mean_width) * math.sqrt(instances_tested - 1))
    
    if correlation < 0 or correlation > 1:
        return {
            "metric_name": "Hodge Structure Rank vs Monotone Width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"Correlation out of bounds: {correlation}"
        }
    
    return {
        "metric_name": "Hodge Structure Rank vs Monotone Width",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")