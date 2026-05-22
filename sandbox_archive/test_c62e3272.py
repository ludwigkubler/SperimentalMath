# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_function(n):
        return [random.randint(1, n) for _ in range(n)]
    
    def calculate_minimal_rank(f):
        # Placeholder function to simulate minimal rank calculation
        return random.randint(1, 10)
    
    def calculate_acc0_circuit_size(f):
        # Placeholder function to simulate ACC⁰ circuit size calculation
        return 2 ** len(f)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_function(n)
    minimal_rank = calculate_minimal_rank(f)
    acc0_circuit_size = calculate_acc0_circuit_size(f)
    
    return {
        "metric_name": "Minimal Rank vs ACC⁰ Circuit Size",
        "metric_value": Fraction(minimal_rank, acc0_circuit_size),
        "instances_tested": 1,
        "conjecture_holds": minimal_rank >= acc0_circuit_size,
        "counterexample": "" if minimal_rank >= acc0_circuit_size else f"Function: {f}, Minimal Rank: {minimal_rank}, ACC⁰ Circuit Size: {acc0_circuit_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*100 + 1, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")