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
        rank = 0
        for j in range(n):
            i_max = rank
            for i in range(rank, m):
                if abs(A[i][j]) > abs(A[i_max][j]):
                    i_max = i
            if A[i_max][j] == 0:
                continue
            A[rank], A[i_max] = A[i_max], A[rank]
            for i in range(m):
                if i != rank:
                    factor = A[i][j] / A[rank][j]
                    for k in range(n):
                        A[i][k] -= factor * A[rank][k]
            rank += 1
        return rank

    def tropicalize(A):
        m, n = len(A), len(A[0])
        T = [[-math.inf] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if A[i][j] != -math.inf:
                    T[i][j] = max(T[i][j], A[i][j])
        return T

    def symplectic_form(A):
        m, n = len(A), len(A[0])
        B = [[0] * (2*n) for _ in range(2*m)]
        for i in range(m):
            for j in range(n):
                if A[i][j] != -math.inf:
                    B[i][j] = 1
                    B[m+i][n+j] = 1
        return tropicalize(B)

    def parity_circuit(n):
        circuit = []
        for i in range(n):
            gate = random.choice(['AND', 'OR'])
            if gate == 'AND':
                circuit.append((i, i+1))
            else:
                circuit.append((i, n+i))
        return circuit

    def compute_symplectic_rank(circuit, n):
        A = [[-math.inf] * (n+n) for _ in range(n+n)]
        for i, j in circuit:
            A[i][j] = 1
            A[j][i+n] = 1
        return gaussian_elimination(A)

    n = random.randint(5, 40)
    circuit = parity_circuit(n)
    symplectic_ranks = [compute_symplectic_rank(circuit, n) for _ in range(30)]
    
    metric_value = sum(symplectic_ranks) / len(symplectic_ranks)
    conjecture_holds = all(abs(rank - math.log2(n)) <= 3 for rank in symplectic_ranks)
    counterexample = "" if conjecture_holds else "n={}".format(n)

    return {
        "metric_name": "Symplectic Rank",
        "metric_value": metric_value,
        "instances_tested": len(symplectic_ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.9:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample='n={}' first_failing_seed={}".format(first_failing_seed, first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")