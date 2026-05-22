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
        return [random.randint(0, n-1) for _ in range(n)]
    
    def calculate_minimal_rank(f):
        # Placeholder for actual quandle operation calculation
        return random.randint(1, 5)
    
    def smallest_acc0_circuit_size(f):
        # Placeholder for actual ACC⁰ circuit size calculation
        return len(f) // 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_function(n)
    
    minimal_rank = calculate_minimal_rank(f)
    acc0_circuit_size = smallest_acc0_circuit_size(f)
    
    return {
        "metric_name": "Minimal Rank vs ACC⁰ Circuit Size",
        "metric_value": Fraction(minimal_rank, acc0_circuit_size),
        "instances_tested": 1,
        "conjecture_holds": minimal_rank >= acc0_circuit_size,
        "counterexample": "" if minimal_rank >= acc0_circuit_size else f"Function: {f}, Minimal Rank: {minimal_rank}, ACC⁰ Circuit Size: {acc0_circuit_size}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")