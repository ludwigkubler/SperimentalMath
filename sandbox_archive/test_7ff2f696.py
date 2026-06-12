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
    
    def generate_circuit(depth):
        if depth == 1:
            return random.choice(['0', '1'])
        else:
            sub_depth = random.randint(1, depth-1)
            left = generate_circuit(sub_depth)
            right = generate_circuit(depth - sub_depth - 1)
            return f"({left} & {right})"
    
    def evaluate_circuit(circuit):
        if circuit == '0':
            return [0]
        elif circuit == '1':
            return [1]
        else:
            left, op, right = circuit[1:-1].split(' ')
            left_vals = evaluate_circuit(left)
            right_vals = evaluate_circuit(right)
            if op == '&':
                return [x & y for x in left_vals for y in right_vals]
    
    def frobenius_coincidence(values):
        n = len(values)
        count = 0
        for i in range(n):
            for j in range(i+1, n):
                if values[i] == values[j]:
                    count += 1
        return count
    
    max_frob_rank = 0
    instances_tested = 0
    n_max = 1
    
    for depth in [5, 10, 15, 20, 30, 40]:
        if instances_tested >= 30:
            break
        
        circuit = generate_circuit(depth)
        values = evaluate_circuit(circuit)
        frob_rank = frobenius_coincidence(values)
        
        max_frob_rank = max(max_frob_rank, frob_rank)
        instances_tested += 1
        n_max = max(n_max, depth)
    
    if instances_tested < 30:
        return {
            "metric_name": "max_frob_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    metric_value = max_frob_rank
    conjecture_holds = (metric_value <= 1.25 * depth ** 2 for depth in [5, 10, 15, 20, 30, 40])
    
    return {
        "metric_name": "max_frob_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(conjecture_holds),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "unknown"
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)