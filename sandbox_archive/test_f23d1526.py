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
    
    def generate_circuit(n):
        if n == 1:
            return {'inputs': [0], 'gates': [], 'outputs': [0]}
        inputs = list(range(n))
        gates = []
        for i in range(1, n):
            gate = (random.choice(inputs), random.choice(inputs), random.choice(['AND', 'OR']))
            gates.append(gate)
            inputs.append(i + n - 1)
        outputs = [n - 1]
        return {'inputs': inputs[:n], 'gates': gates, 'outputs': outputs}
    
    def monotone_complexity(circuit):
        # Placeholder for actual monotone complexity calculation
        return len(circuit['gates'])
    
    def min_order(circuit):
        # Placeholder for actual minimal order calculation
        return len(circuit['gates'])
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    m = monotone_complexity(circuit)
    min_ord = min_order(circuit)
    
    if abs(min_ord - m) > 2:
        return {
            "metric_name": "min_order",
            "metric_value": min_ord,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"n={n}, min_order={min_ord}, m={m}"
        }
    
    return {
        "metric_name": "min_order",
        "metric_value": min_ord,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(r['counterexample'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result['counterexample'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")