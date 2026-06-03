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
    
    def generate_circuit(n, k):
        # Simple DPLL-based solver to generate a monotone circuit
        if n == 1 and k == 0:
            return []
        elif n == 1 and k == 1:
            return [[random.choice([1, -1])]]
        else:
            literals = [i for i in range(1, n+1)]
            random.shuffle(literals)
            circuit = []
            for _ in range(k):
                clause = [literals.pop()]
                while len(clause) < 2 and literals:
                    clause.append(literals.pop())
                circuit.append(clause)
            return circuit
    
    def compute_graphical_motive(circuit):
        # Simplified graphical motive computation
        n = len(circuit[0])
        M = [[0] * n for _ in range(n)]
        for clause in circuit:
            for lit1 in clause:
                for lit2 in clause:
                    if abs(lit1) != abs(lit2):
                        M[abs(lit1)-1][abs(lit2)-1] += 1
        return M
    
    def matrix_rank(M):
        # Gaussian elimination to compute the rank of a matrix
        n = len(M)
        rank = n
        for i in range(n):
            if M[i][i] == 0:
                reduce = False
                for k in range(i+1, n):
                    if M[k][i] != 0:
                        M[i], M[k] = M[k], M[i]
                        reduce = True
                        break
                if not reduce:
                    rank -= 1
                    continue
            for j in range(n):
                if i != j and M[j][i] != 0:
                    factor = -M[j][i] / M[i][i]
                    for k in range(n):
                        M[j][k] += factor * M[i][k]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    min_rank = float('inf')
    max_n = 0
    
    for n in n_values:
        for _ in range(5):
            k = random.randint(0, n)
            circuit = generate_circuit(n, k)
            M = compute_graphical_motive(circuit)
            rank = matrix_rank(M)
            instances_tested += 1
            min_rank = min(min_rank, rank)
            max_n = max(max_n, n)
    
    epsilon = 0.1
    conjecture_holds = abs(min_rank - (k**2 * math.log(n))) <= epsilon
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")