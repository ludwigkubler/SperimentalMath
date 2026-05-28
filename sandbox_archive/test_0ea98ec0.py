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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = A[i][i]
        if factor == 0:
            continue
        for j in range(n):
            A[i][j] /= factor
        for j in range(m):
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def compute_minimal_rank(circuit):
    n = len(circuit)
    Q = [[0] * (n + 1) for _ in range(n + 1)]
    for i, gate in enumerate(circuit):
        x, y = gate
        Q[x][y] += 1
        Q[y][x] -= 1
    rank = gaussian_elimination(Q)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([10, 20, 30, 40])
    instances_tested = 30
    total_rank = 0
    
    for _ in range(instances_tested):
        circuit = []
        for _ in range(n):
            x = random.randint(0, n-1)
            y = random.randint(0, n-1)
            while x == y:
                y = random.randint(0, n-1)
            circuit.append((x, y))
        
        rank = compute_minimal_rank(circuit)
        total_rank += rank
    
    avg_rank = total_rank / instances_tested
    conjecture_holds = abs(avg_rank - math.sqrt(n)) <= 0.3 * math.sqrt(n) and (math.sqrt(n) - 10 * math.sqrt(n) / 100) <= avg_rank <= (math.sqrt(n) + 10 * math.sqrt(n) / 100)
    counterexample = "" if conjecture_holds else f"avg_rank={avg_rank}, sqrt(n)={math.sqrt(n)}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": avg_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - avg_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")