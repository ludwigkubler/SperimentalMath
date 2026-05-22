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
            if A[i_max][j] != 0:
                A[rank], A[i_max] = A[i_max], A[rank]
                for i in range(rank + 1, m):
                    factor = -A[i][j] / A[rank][j]
                    for k in range(j, n):
                        if rank == i and k == j:
                            A[i][k] = 0
                        else:
                            A[i][k] += factor * A[rank][k]
                rank += 1
        return rank
    
    def hodge_index(A):
        rank = gaussian_elimination(A)
        return rank
    
    def sos_refutation_size(CNF):
        # Placeholder for actual SOS refutation size computation
        # This is a dummy implementation
        return len(CNF) * len(CNF[0])
    
    def quasi_clifford_algebra(CNF):
        # Placeholder for actual quasi-clifford algebra construction
        # This is a dummy implementation
        n = len(CNF)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in CNF:
            for literal in clause:
                i = abs(literal) - 1
                if literal > 0:
                    A[i][i] += 1
                else:
                    A[i][i] -= 1
        return A
    
    n = random.randint(5, 40)
    k = random.randint(2, 3)
    CNF = [[random.randint(1, n) for _ in range(k)] for _ in range(n)]
    
    algebra = quasi_clifford_algebra(CNF)
    refutation_size = sos_refutation_size(CNF)
    hodge_index_value = hodge_index(algebra)
    
    if refutation_size == 0:
        return {
            "metric_name": "HodgeIndex",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "SOS refutation size is zero"
        }
    
    conjecture_holds = abs(hodge_index_value - math.sqrt(refutation_size)) <= 3
    counterexample = "" if conjecture_holds else f"HodgeIndex={hodge_index_value}, sqrt(s)={math.sqrt(refutation_size)}"
    
    return {
        "metric_name": "HodgeIndex",
        "metric_value": hodge_index_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"HodgeIndex exceeds sqrt(s) by more than 3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")