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
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def minimal_rank(M):
        d = len(M)
        A = [[M[i][j] for j in range(d)] for i in range(d)]
        return gaussian_elimination(A)
    
    def xor_and_circuit(n):
        if n == 1:
            return [0, 1]
        else:
            left = xor_and_circuit(n // 2)
            right = xor_and_circuit(n - n // 2)
            return [a ^ b for a in left] + [a & b for a in left] + [a ^ b for b in right] + [a & b for b in right]
    
    def monodromy_representation(circuit):
        d = len(circuit)
        M = [[0] * d for _ in range(d)]
        for i in range(d):
            if circuit[i] == 0:
                M[i][i] = 1
            elif circuit[i] == 1:
                for j in range(i + 1, d):
                    M[i][j] = 1
                    M[j][i] = 1
        return M
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = xor_and_circuit(n)
            M = monodromy_representation(circuit)
            rank = minimal_rank(M)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank <= n ** 2 * math.log(n)
    
    return {
        "metric_name": "Minimal Rank of Monodromy Representation",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean rank {mean_rank} exceeds bound {n ** 2 * math.log(n)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank exceeds bound\" first_failing_seed={first_failing_seed}")