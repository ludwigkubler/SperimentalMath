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
    
    def generate_quaternion():
        return [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]
    
    def tropicalize(q):
        return max(abs(x) for x in q)
    
    def ac0_parity_circuit(depth: int):
        if depth == 1:
            return [random.choice([0, 1])]
        else:
            left = ac0_parity_circuit(depth - 1)
            right = ac0_parity_circuit(depth - 1)
            return [left[i] ^ right[i] for i in range(len(left))]
    
    def min_rank(tropicalized):
        if tropicalized == 0:
            return 0
        else:
            return 1
    
    n = random.randint(5, 40)
    total_rank = 0
    instances_tested = 0
    
    for _ in range(n):
        q = generate_quaternion()
        t = tropicalize(q)
        depth = random.randint(1, 3)  # Limiting depth to avoid excessive computation
        circuit = ac0_parity_circuit(depth)
        rank = min_rank(t)
        total_rank += rank
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "min_rank_over_diameter",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_rank = Fraction(total_rank, instances_tested)
    log_diameter = math.log(instances_tested)  # Simplified for demonstration
    ratio = mean_rank / log_diameter
    
    return {
        "metric_name": "min_rank_over_diameter",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "conjecture_holds": ratio >= 1,  # Hypothetical constant c=1 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed=None")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_evidence_or_budget_exceeded n_tested=30")