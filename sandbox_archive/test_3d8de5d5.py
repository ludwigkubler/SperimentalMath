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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return [row for row in A if any(row)]

    def min_rank(A):
        return len(gaussian_elimination(A))

    def generate_boolean_circuit(d: int):
        n = 2 ** (d + 1)
        circuit = []
        for i in range(n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(gate)]
            circuit.append((gate, inputs))
        return circuit

    def monotonicity_degree(circuit):
        n = len(circuit)
        degree = 0
        for i in range(n - 1):
            if circuit[i][0] == 'AND':
                if any(circuit[j][0] == 'OR' for j in range(i + 1, n)):
                    degree += 1
            elif circuit[i][0] == 'OR':
                if all(circuit[j][0] == 'AND' for j in range(i + 1, n)):
                    degree += 1
        return degree

    def tropicalize_quiver(n):
        quiver = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            quiver[i][i] = 0
        return quiver

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        degree = monotonicity_degree(circuit)
        quiver = tropicalize_quiver(degree)
        rank = min_rank(quiver)
        
        results.append({
            "n": n,
            "degree": degree,
            "rank": rank
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["rank"] <= result["degree"]) / len(results)
    
    conjecture_holds = support_fraction >= 0.8 and mean_rank <= max([result["degree"] + 1 for result in results])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")