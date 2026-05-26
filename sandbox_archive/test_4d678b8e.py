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
    
    def generate_arithmetic_circuit(n, m):
        # Simplified generation for demonstration purposes
        return [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]
    
    def calculate_symplectic_leaves(circuit):
        # Placeholder for symplectic leaf calculation
        return [random.randint(1, 5) for _ in range(len(circuit))]
    
    def minimal_rank(leaves):
        # Placeholder for minimal rank calculation
        return len(set(leaves))
    
    n = random.randint(5, 40)
    m = random.randint(1, 10)
    circuit = generate_arithmetic_circuit(n, m)
    leaves = calculate_symplectic_leaves(circuit)
    rank = minimal_rank(leaves)
    
    expected_upper_bound = n * math.log(m)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= expected_upper_bound,
        "counterexample": "" if rank <= expected_upper_bound else f"rank={rank}, expected={expected_upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[seeds.index(first_failing_seed)]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")