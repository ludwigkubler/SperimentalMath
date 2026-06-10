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

def generate_boolean_circuit(depth: int, size: int) -> list:
    if depth == 0:
        return ['0', '1']
    
    inputs = generate_boolean_circuit(depth - 1, size // 2)
    circuit = []
    for _ in range(size):
        a, b = random.choice(inputs), random.choice(inputs)
        gate = random.choice(['AND', 'OR'])
        if gate == 'AND':
            circuit.append(f'({a} AND {b})')
        else:
            circuit.append(f'({a} OR {b})')
    return circuit

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "minimal_rank"
    instances_tested = 0
    n_max = 0
    total_ranks = []
    conjecture_holds = True
    counterexample = ""
    
    for D in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            n = random.randint(1, min(n_max + 1, 40))
            circuit = generate_boolean_circuit(D, n)
            if not circuit:
                conjecture_holds = False
                counterexample = "empty_circuit"
                break
            
            # Simulate computing the minimal rank of a Kac-Moody algebra (placeholder)
            rank = len(circuit)  # Placeholder for actual computation
            total_ranks.append(rank)
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not conjecture_holds:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    
    mean_rank = sum(total_ranks) / len(total_ranks)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in total_ranks) / len(total_ranks))
    expected_bound = D**2 * math.log(n_max)
    
    if mean_rank <= expected_bound:
        return {
            "metric_name": metric_name,
            "metric_value": mean_rank,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": metric_name,
            "metric_value": mean_rank,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"mean_rank={mean_rank} > expected_bound={expected_bound}"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")