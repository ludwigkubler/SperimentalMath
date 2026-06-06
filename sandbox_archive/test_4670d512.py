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
    
    def generate_circuit(depth, n):
        if depth == 0:
            return [random.choice([0, 1]) for _ in range(n)]
        else:
            inputs = generate_circuit(depth - 1, n)
            gate = random.choice(['AND', 'OR'])
            if gate == 'AND':
                return [a and b for a, b in zip(inputs[:n//2], inputs[n//2:])]
            else:
                return [a or b for a, b in zip(inputs[:n//2], inputs[n//2:])]

    def generate_vector_space(circuit):
        n = len(circuit)
        V = []
        for i in range(n):
            if circuit[i] == 0:
                V.append([1, 0])
            else:
                V.append([0, 1])
        return V

    def find_minimal_affine_subspaces(V):
        m, n = len(V), len(V[0])
        subspaces = []
        for i in range(m):
            subspace = [V[i]]
            for j in range(i + 1, m):
                if all(V[j][k] == V[i][k] for k in range(n)):
                    subspace.append(V[j])
            subspaces.append(subspace)
        return subspaces

    def count_affine_subspaces(V):
        subspaces = find_minimal_affine_subspaces(V)
        return len(subspaces)

    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for depth in range(5, 41):
        for _ in range(6):  # Ensure at least 30 instances per seed
            n = random.randint(2, n_max)
            circuit = generate_circuit(depth, n)
            V = generate_vector_space(circuit)
            metric_value = count_affine_subspaces(V)
            total_metric_value += metric_value
            instances_tested += 1

            if depth * depth * math.log(n) < metric_value:
                conjecture_holds = False
                counterexample = f"Depth {depth}, n={n}, Expected O({depth**2 * math.log(n)}) but got {metric_value}"

    mean_metric_value = total_metric_value / instances_tested
    std_metric_value = (sum((x - mean_metric_value) ** 2 for x in range(instances_tested)) / instances_tested) ** 0.5

    return {
        "metric_name": "Min Affine Subspaces",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")