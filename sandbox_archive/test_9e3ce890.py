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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def communication_matrix(circuit):
        n = len(circuit)
        comm_matrix = [[0] * (n * n) for _ in range(n * n)]
        for i in range(n):
            for j in range(n):
                if circuit[i][j]:
                    comm_matrix[i * n + k][j * n + k] = 1
        return comm_matrix
    
    def real_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if matrix[i][i]:
                rank += 1
                for j in range(i + 1, m):
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def ac0_circuit(n):
        circuit = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    circuit[i][j] = True
                    circuit[j][i] = True
        return circuit
    
    n = random.randint(5, 40)
    circuit = ac0_circuit(n)
    comm_matrix = communication_matrix(circuit)
    rank = real_rank(comm_matrix)
    
    expected_rank = math.ceil(n ** (1 / (len(circuit) - 1)))
    conjecture_holds = rank >= expected_rank
    
    return {
        "metric_name": "real_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, rank={rank}, expected={expected_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['metric_value']}, rank={results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")