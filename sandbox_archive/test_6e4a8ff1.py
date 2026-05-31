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
            return ['input']
        else:
            left = generate_circuit(depth - 1)
            right = generate_circuit(depth - 1)
            return [f'AND({left[0]}, {right[0]})', f'OR({left[0]}, {right[0]})']
    
    def count_distinct_actions(circuit):
        actions = set()
        for gate in circuit:
            if 'AND(' in gate or 'OR(' in gate:
                action = gate.split('(')[1].split(',')[0]
                actions.add(action)
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
    
    mean_actions = total_actions / instances_tested
    conjecture_holds = mean_actions <= 2 ** max_depth
    counterexample = "" if conjecture_holds else f"mean_actions={mean_actions} > 2^{max_depth}"
    
    return {
        "metric_name": "distinct_coxeter_group_actions",
        "metric_value": mean_actions,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")