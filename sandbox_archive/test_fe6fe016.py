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
    
    def generate_circuit(n, m):
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def transform_circuit(circuit):
        moves = 0
        while True:
            changed = False
            for i in range(len(circuit)):
                gate_type, inputs = circuit[i]
                if gate_type == 'AND':
                    new_input = all(inputs)
                elif gate_type == 'OR':
                    new_input = any(inputs)
                if new_input != inputs[0]:
                    circuit[i] = (gate_type, [new_input])
                    moves += 1
                    changed = True
            if not changed:
                break
        return moves
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_moves = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n, 2 * n)
            circuit = generate_circuit(n, m)
            moves = transform_circuit(circuit)
            total_moves += moves
            instances_tested += 1
            if n > n_max:
                n_max = n
    
    metric_value = total_moves / instances_tested
    conjecture_holds = metric_value >= m ** (2/3)
    counterexample = "" if conjecture_holds else f"m={m}, moves={moves}"
    
    return {
        "metric_name": "Moves Required",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")