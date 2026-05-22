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

def gaussian_elimination(A, b):
    n = len(b)
    augmented = [[A[i][j] for j in range(n)] + [b[i]] for i in range(n)]
    
    for i in range(n):
        # Find pivot row
        max_row = i
        for k in range(i+1, n):
            if abs(augmented[k][i]) > abs(augmented[max_row][i]):
                max_row = k
        
        # Swap rows
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        
        # Eliminate below pivot
        for k in range(i+1, n):
            factor = augmented[k][i] / augmented[i][i]
            for j in range(n + 1):
                augmented[k][j] -= factor * augmented[i][j]
    
    # Back-substitute to find solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = augmented[i][-1]
        for j in range(i+1, n):
            x[i] -= augmented[i][j] * x[j]
        x[i] /= augmented[i][i]
    
    return x

def compute_quandle_rank(gates):
    A = []
    b = []
    for gate in gates:
        row = [0] * len(gate)
        row[gate[1]] = 1
        A.append(row)
        b.append(-gate[2])
    
    try:
        solution = gaussian_elimination(A, b)
        rank = sum(1 for x in solution if not math.isclose(x, 0))
        return rank
    except ZeroDivisionError:
        return None

def generate_xor_and_network(n):
    gates = []
    inputs = [i for i in range(n)]
    outputs = [n + i for i in range(n)]
    
    # Generate random XOR-AND gates
    for _ in range(2 * n):
        gate_type = random.choice(['XOR', 'AND'])
        if gate_type == 'XOR':
            inputs1, inputs2 = random.sample(inputs, 2)
            output = random.choice(outputs)
            gates.append((inputs1, inputs2, output))
        else:
            inputs1, inputs2 = random.sample(inputs, 2)
            output = random.choice(outputs)
            gates.append((inputs1, inputs2, output))
    
    return gates

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    gates = generate_xor_and_network(n)
    
    quandle_rank = compute_quandle_rank(gates)
    if quandle_rank is None:
        return {
            "metric_name": "Quandle Rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_n_squared = math.log(n, 2) ** 2
    conjecture_holds = quandle_rank <= log_n_squared
    
    return {
        "metric_name": "Quandle Rank",
        "metric_value": quandle_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"quandle_rank={quandle_rank}, log^2(n)={log_n_squared}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"quandle_rank > log^2(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")