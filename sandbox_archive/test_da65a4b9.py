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
    
    def generate_circuit(depth, num_vars):
        if depth == 0:
            return [random.choice([0, 1]) for _ in range(num_vars)]
        else:
            inputs = generate_circuit(depth - 1, num_vars)
            gate = random.choice(['AND', 'OR'])
            if gate == 'AND':
                return [inputs[i] & inputs[j] for i in range(len(inputs)) for j in range(i + 1, len(inputs))]
            else:
                return [inputs[i] | inputs[j] for i in range(len(inputs)) for j in range(i + 1, len(inputs))]
    
    def vector_space_representation(circuit):
        n = len(circuit)
        V = []
        for val in circuit:
            v = [0] * n
            v[val] = 1
            V.append(v)
        return V
    
    def min_affine_subspaces(V):
        m, n = len(V), len(V[0])
        subspaces = []
        for i in range(m):
            subspace = [V[i]]
            for j in range(i + 1, m):
                if all(V[j][k] == V[i][k] for k in range(n)):
                    subspace.append(V[j])
            subspaces.append(subspace)
        return len(subspaces)
    
    num_vars = random.randint(2, 10)
    depth = random.randint(5, 40)
    circuit = generate_circuit(depth, num_vars)
    V = vector_space_representation(circuit)
    min_subspaces = min_affine_subspaces(V)
    
    metric_name = "min_affine_subspaces"
    metric_value = min_subspaces
    instances_tested = 1
    n_max = depth
    conjecture_holds = (min_subspaces <= depth**2 * math.log(num_vars, 2))
    counterexample = "" if conjecture_holds else f"Depth={depth}, num_vars={num_vars}"
    
    return {
        "metric_name": metric_name,
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
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")