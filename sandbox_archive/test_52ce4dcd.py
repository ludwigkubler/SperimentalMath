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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def rank(A):
        rref = gaussian_elimination(A)
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank

    def xor_and(n):
        inputs = [tuple(random.randint(0, 1) for _ in range(n)) for _ in range(2**n)]
        outputs = [sum(inputs[i]) % 2 for i in range(2**n)]
        return inputs, outputs

    def quadratic_form_rank(inputs, outputs):
        n = len(inputs[0])
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for x, y in zip(inputs, outputs):
            A[-1][-1] += y
            for i in range(n):
                A[i][-1] += x[i]
                for j in range(i, n):
                    A[i][j] += x[i] * x[j]
        return rank(A)

    def ac0_circuit_size(circuit):
        if not circuit:
            return 0
        return max(ac0_circuit_size(subcircuit) for subcircuit in circuit) + 1

    n = random.randint(5, 40)
    inputs, outputs = xor_and(n)
    size = ac0_circuit_size(inputs)
    epsilon = 0.1
    min_rank = float('inf')
    
    for _ in range(30):
        q_rank = quadratic_form_rank(inputs, outputs)
        if q_rank < min_rank:
            min_rank = q_rank
    
    conjecture_holds = min_rank >= math.log2(size) + epsilon
    counterexample = "" if conjecture_holds else f"n={n}, size={size}, min_rank={min_rank}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")