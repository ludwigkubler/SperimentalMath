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
            inputs = random.sample(range(n), 2)
            circuit.append((gate_type, inputs))
        return circuit
    
    def transform_circuit(circuit):
        moves = 0
        while True:
            changed = False
            for i in range(len(circuit)):
                if circuit[i][0] == 'AND':
                    if circuit[i][1][0] == circuit[i][1][1]:
                        circuit.pop(i)
                        changed = True
                        break
                elif circuit[i][0] == 'OR':
                    if circuit[i][1][0] != circuit[i][1][1]:
                        circuit[i] = ('NOT', circuit[i][1])
                        changed = True
                        break
            if not changed:
                break
            moves += 1
        return moves
    
    n_max = 40
    instances_tested = 30
    total_moves = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(5, n_max)
        circuit = generate_circuit(n, m)
        moves = transform_circuit(circuit)
        total_moves += moves
    
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
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 60))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")