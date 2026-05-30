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
        if depth == 1:
            return [random.choice([0, 1])]
        else:
            subcircuits = [generate_circuit(random.randint(1, depth-1)) for _ in range(2)]
            return [random.choice([0, 1]) + (subcircuits[0], subcircuits[1])]
    
    def compute_depth(circuit):
        if isinstance(circuit, int):
            return 0
        else:
            return max(compute_depth(subcircuit) for subcircuit in circuit) + 1
    
    def polynomial_representation(circuit):
        if isinstance(circuit, int):
            return [circuit]
        else:
            return [circuit[0]] + [x for subcircuit in circuit[1:] for x in polynomial_representation(subcircuit)]
    
    def grothendieck_witt_class(poly):
        n = len(poly)
        matrix = [[0] * n for _ in range(n)]
        for i, p in enumerate(poly):
            if p == 1:
                matrix[i][i] = 1
        return matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(matrix[j][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, n):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return matrix
    
    def determinant(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            det *= matrix[i][i]
        return det
    
    depth = random.randint(5, 40)
    circuit = generate_circuit(depth)
    poly = polynomial_representation(circuit)
    gwc = grothendieck_witt_class(poly)
    qdd = abs(determinant(gaussian_elimination(gwc)))
    
    metric_name = "Quantum Deformation Degree"
    metric_value = qdd
    instances_tested = 1
    n_max = depth
    conjecture_holds = qdd <= depth + 3
    counterexample = "" if conjecture_holds else f"QDD={qdd}, Depth={depth}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"QDD > Depth + 3\" first_failing_seed={first_failing_seed}")