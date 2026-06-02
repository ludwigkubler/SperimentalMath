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
    
    def generate_boolean_circuit(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            subcircuits = [generate_boolean_circuit(random.randint(1, n-1)) for _ in range(2)]
            gate = random.choice(['AND', 'OR'])
            return [gate] + subcircuits

    def state_space_representation(circuit):
        if isinstance(circuit[0], int):
            return {tuple(circuit)}
        else:
            gate = circuit[0]
            left, right = circuit[1:]
            left_states = state_space_representation(left)
            right_states = state_space_representation(right)
            if gate == 'AND':
                return {(x & y for x in left_states for y in right_states)
                        if isinstance(x, int) and isinstance(y, int) else (x, y)}
            elif gate == 'OR':
                return {(x | y for x in left_states for y in right_states)
                        if isinstance(x, int) and isinstance(y, int) else (x, y)}

    def minimal_polynomial(state_space):
        n = len(state_space[0])
        m = 2 ** n
        A = [[0] * m for _ in range(m)]
        b = [0] * m
        
        for state in state_space:
            index = sum(1 << i if bit else 0 for i, bit in enumerate(reversed(state)))
            A[index][index] += 1
            for j in range(m):
                if (j & index) == 0:
                    A[j][index] += 1
                    b[j] += 1
        
        for i in range(m):
            if A[i][i] == 0:
                return None  # Singular matrix, no minimal polynomial
        
        for i in range(m):
            if i != A[i].index(max(A[i])):
                A[i], A[A[i].index(max(A[i]))] = A[A[i].index(max(A[i]))], A[i]
        
        for i in range(m):
            factor = 1 / A[i][i]
            A[i] = [x * factor for x in A[i]]
            b[i] *= factor
        
        for i in range(m-1, -1, -1):
            for j in range(i-1, -1, -1):
                factor = A[j][i]
                A[j] = [A[j][k] - factor * A[i][k] for k in range(m)]
                b[j] -= factor * b[i]
        
        return b

    def topological_entropy(state_space):
        n = len(state_space[0])
        m = 2 ** n
        transitions = [[0] * m for _ in range(m)]
        
        for i in range(m):
            for j in range(m):
                if (i & j) == 0:
                    transitions[i][j] += 1
        
        total_transitions = sum(sum(row) for row in transitions)
        entropy = -sum(p * math.log2(p) for p in [sum(transitions[i]) / total_transitions for i in range(m)]) if total_transitions > 0 else 0
        return entropy

    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_boolean_circuit(n)
        state_space = state_space_representation(circuit)
        m = len(state_space[0])
        
        if m == 1:
            continue
        
        poly = minimal_polynomial(state_space)
        if poly is None:
            continue
        
        entropy = topological_entropy(state_space)
        metric_values.append(entropy * math.log2(m))
    
    if not metric_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    correlation_coefficient = mean / std_dev if std_dev != 0 else 0
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")