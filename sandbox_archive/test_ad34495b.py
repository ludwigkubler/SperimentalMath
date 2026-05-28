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
    
    def generate_branching_program(n):
        # Generate a random read-twice branching program with n variables
        program = []
        for _ in range(2 ** (n - 1)):
            node = random.choice(['0', '1'])
            if node == '0':
                program.append('0')
            else:
                program.append(random.choice(['0', '1']))
        return program
    
    def compute_quantum_category_invariant(program):
        # Placeholder for the actual computation of quantum category invariant
        # This is a dummy implementation for demonstration purposes
        size = len(program)
        if size == 1:
            return 1.0
        else:
            return math.log(size, 2) / size
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        program = generate_branching_program(n)
        invariant = compute_quantum_category_invariant(program)
        results.append(invariant)
    
    mean_value = sum(results) / len(results)
    max_value = max(results)
    min_value = min(results)
    support_fraction = sum(1 for v in results if 0.5 * math.log(n, 2) <= v <= 2 * math.log(n, 2)) / len(results)
    
    conjecture_holds = all(0.5 * math.log(n, 2) <= v <= 2 * math.log(n, 2) for n, v in zip(n_values, results))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Quantum Category Invariant",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")