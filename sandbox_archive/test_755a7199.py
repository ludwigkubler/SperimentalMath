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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            raise ValueError("Matrix is singular")
        for j in range(i, n):
            A[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
    rank = sum(1 for row in A if any(row[j] != 0 for j in range(n)))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random ACC⁰ circuit of size s
    n = random.randint(5, 40)
    s = random.randint(1, 20)
    circuit = []
    for _ in range(s):
        gate_type = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, n-1) for _ in range(gate_type == 'OR')]
        circuit.append((gate_type, inputs))
    
    # Construct the tropical graph G
    V = list(range(n))
    E = []
    for i in range(s):
        gate_type, inputs = circuit[i]
        if gate_type == 'AND':
            for j in range(i+1, s):
                if all(inputs[k] in circuit[j][1] for k in range(len(inputs))):
                    E.append((inputs[0], inputs[1]))
        elif gate_type == 'OR':
            for j in range(i+1, s):
                if any(inputs[k] in circuit[j][1] for k in range(len(inputs))):
                    E.append((inputs[0], inputs[1]))
    
    G = (V, E)
    
    # Compute the rank of the vertex set of G
    rank = gaussian_elimination(G)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= s * math.log(n),
        "counterexample": "" if rank <= s * math.log(n) else "Rank exceeds expected bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Rank exceeds expected bound' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")