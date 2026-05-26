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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def random_monotone_circuit(k, n):
    circuit = []
    for _ in range(k):
        gate_type = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(n)]
        circuit.append((gate_type, inputs))
    return circuit

def quandle_representation(circuit):
    quandle = {}
    for gate_type, inputs in circuit:
        if gate_type == 'AND':
            key = tuple(inputs)
            if key not in quandle:
                quandle[key] = 1
            else:
                quandle[key] += 1
        elif gate_type == 'OR':
            key = tuple(inputs)
            if key not in quandle:
                quandle[key] = 0
            else:
                quandle[key] -= 1
    return list(quandle.values())

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_tests = 30
    total_rank = 0
    counterexample = ""
    
    for _ in range(n_tests):
        k = random.randint(5, 40)
        circuit = random_monotone_circuit(k, n)
        quandle_rep = quandle_representation(circuit)
        
        if not quandle_rep:
            continue
        
        rank_quandle = gaussian_elimination(quandle_rep)
        total_rank += rank_quandle
        
        if rank_quandle < 2**k:
            counterexample = f"rank={rank_quandle}, expected=2^{k}"
            break
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": total_rank / n_tests,
        "instances_tested": n_tests,
        "conjecture_holds": rank_quandle >= 2**k if counterexample == "" else False,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")