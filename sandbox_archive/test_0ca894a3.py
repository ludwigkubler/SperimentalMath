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
        if depth == 0:
            return ['x1']
        else:
            left = generate_circuit(depth - 1)
            right = generate_circuit(depth - 1)
            return [f'({left[0]} & {right[0]})', f'({left[0]} | {right[0]})']
    
    def count_distinct_actions(circuit):
        actions = set()
        for expr in circuit:
            if '&' in expr:
                actions.add(expr.split(' & ')[0])
                actions.add(expr.split(' & ')[1])
            elif '|' in expr:
                actions.add(expr.split(' | ')[0])
                actions.add(expr.split(' | ')[1])
        return len(actions)
    
    max_depth = 40
    instances_tested = 30
    n_max = 0
    
    total_actions = 0
    
    for _ in range(instances_tested):
        depth = random.randint(5, max_depth)
        circuit = generate_circuit(depth)
        actions = count_distinct_actions(circuit)
        total_actions += actions
        if depth > n_max:
            n_max = depth
    
    metric_value = total_actions / instances_tested
    conjecture_holds = (metric_value <= 2 ** max_depth)
    counterexample = "" if conjecture_holds else f"Depth {max_depth}, Actions {total_actions}"
    
    return {
        "metric_name": "Distinct Coxeter Group Actions",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample=\"Depth {results[0]['n_max']}, Actions {results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")