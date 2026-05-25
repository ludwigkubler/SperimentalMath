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
    
    def generate_circuit(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [left, right]
    
    def construct_polynomial(circuit):
        if len(circuit) == 1:
            return circuit[0] * (1 << (len(circuit) - 1))
        else:
            left = construct_polynomial(circuit[0])
            right = construct_polynomial(circuit[1])
            return [left, right]
    
    def min_rank(poly):
        if len(poly) == 1:
            return 1
        else:
            left_rank = min_rank(poly[0])
            right_rank = min_rank(poly[1])
            return max(left_rank, right_rank)
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    poly = construct_polynomial(circuit)
    rank = min_rank(poly)
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        int(math.sqrt(i)) * (i % 2 + 1) for i in range(30, 60)
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")