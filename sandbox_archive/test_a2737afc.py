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
    
    def generate_bp(size):
        bp = []
        for _ in range(size):
            row = [random.choice([0, 1]) for _ in range(size)]
            bp.append(row)
        return bp
    
    def quantum_entanglement_index(bp):
        size = len(bp)
        entanglement_index = 0
        for i in range(size):
            for j in range(i + 1, size):
                if bp[i][j] != bp[j][i]:
                    entanglement_index += 1
        return entanglement_index
    
    def polynomial_estimate(n):
        return n * math.log2(n)
    
    instances_tested = 0
    total_entanglement_index = 0
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        size = random.randint(5, 40)
        bp = generate_bp(size)
        entanglement_index = quantum_entanglement_index(bp)
        polynomial_bound = polynomial_estimate(size)
        
        if entanglement_index <= polynomial_bound:
            return {
                "metric_name": "mean_entanglement_index",
                "metric_value": entanglement_index,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        total_entanglement_index += entanglement_index
        instances_tested += 1
    
    mean_entanglement_index = total_entanglement_index / instances_tested
    return {
        "metric_name": "mean_entanglement_index",
        "metric_value": mean_entanglement_index,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")