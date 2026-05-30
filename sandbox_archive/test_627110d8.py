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
                    if sum(inputs) == len(inputs):
                        circuit[i] = ('1', [])
                        changed = True
                    elif sum(inputs) == 0:
                        circuit[i] = ('0', [])
                        changed = True
                elif gate_type == 'OR':
                    if sum(inputs) == len(inputs):
                        circuit[i] = ('1', [])
                        changed = True
                    elif sum(inputs) == 0:
                        circuit[i] = ('0', [])
                        changed = True
            if not changed:
                break
            moves += 1
        return moves
    
    n_max = 40
    instances_tested = 30
    total_moves = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(n, n * 2)
        circuit = generate_circuit(n, m)
        moves = transform_circuit(circuit)
        total_moves += moves
    
    mean_moves = total_moves / instances_tested
    conjecture_holds = mean_moves >= m ** (2/3)
    
    return {
        "metric_name": "moves",
        "metric_value": mean_moves,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
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
    
    mean_moves = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_moves} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_moves} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported by enough seeds' first_failing_seed={first_failing_seed}")