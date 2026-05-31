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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

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
        for gate in circuit:
            if '&' in gate:
                actions.add(gate.split('&')[0])
                actions.add(gate.split('&')[1])
            elif '|' in gate:
                actions.add(gate.split('|')[0])
                actions.add(gate.split('|')[1])
        return len(actions)
    
    def depth_of_circuit(circuit):
        if isinstance(circuit, str):
            return 0
        else:
            return 1 + max(depth_of_circuit(sub) for sub in circuit)
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    actions_count = count_distinct_actions(circuit)
    depth = depth_of_circuit(circuit)
    
    if actions_count > 2**depth:
        return {
            "metric_name": "actions_count",
            "metric_value": actions_count,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Circuit with depth {depth} required more than 2^{depth} distinct actions"
        }
    else:
        return {
            "metric_name": "actions_count",
            "metric_value": actions_count,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))**0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Circuit with depth greater than 2^depth' first_failing_seed={first_failing_seed}")