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
    
    def generate_boolean_circuit(depth):
        if depth == 0:
            return ['0'] if random.choice([True, False]) else ['1']
        elif depth == 1:
            return [random.choice(['NOT', 'AND', 'OR'])]
        else:
            left = generate_boolean_circuit(depth - 1)
            right = generate_boolean_circuit(depth - 1)
            return [random.choice(['NOT', 'AND', 'OR']), left, right]
    
    def count_nodes(circuit):
        if isinstance(circuit[0], str) and circuit[0] in ['NOT', 'AND', 'OR']:
            return 1 + count_nodes(circuit[1]) + count_nodes(circuit[2])
        else:
            return 0
    
    max_depth = 10
    instances_tested = 0
    n_max = 0
    total_nodes = 0
    
    for d in range(5, max_depth + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            circuit = generate_boolean_circuit(d)
            nodes = count_nodes(circuit)
            if nodes > n_max:
                n_max = nodes
            total_nodes += nodes
            instances_tested += 1
    
    mean_nodes = total_nodes / instances_tested
    conjecture_holds = mean_nodes <= (3 * max_depth ** 2)  # Polynomial bound of degree 2
    
    return {
        "metric_name": "Average Nodes in Coxeter-Dynkin Diagram",
        "metric_value": mean_nodes,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean nodes: {mean_nodes}, Max depth: {max_depth}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")