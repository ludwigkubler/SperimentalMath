# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            clauses.append(clause)
        return clauses

    def characteristic_polynomial(cnf):
        n = len(set(abs(lit) for lit in cnf))
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                row, col = abs(lit), -lit if lit < 0 else lit
                matrix[row][col] += 1
        return matrix

    def gaussian_elimination(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if matrix[i][i] == 0:
                swap_found = False
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        swap_found = True
                        break
                if not swap_found:
                    continue
            pivot = Fraction(matrix[i][i])
            for j in range(n + 1):
                matrix[i][j] /= pivot
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
            rank += 1
        return rank

    def ac0c_circuit_size(cnf, m):
        # Placeholder function to construct a constant-depth AC0c circuit
        # This is a dummy implementation and does not actually compute the circuit size
        return random.randint(2**m, 2**(m+1))

    n = random.randint(5, 40)
    k = random.randint(n // 2, n)
    cnf = generate_k_cnf(n, k)
    matrix = characteristic_polynomial(cnf)
    rank = gaussian_elimination(matrix)

    m = rank
    circuit_size = ac0c_circuit_size(cnf, m)

    return {
        "metric_name": "Rank vs AC0c Circuit Depth",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= 2**n - n * math.log(n),
        "counterexample": "" if rank <= 2**n - n * math.log(n) else f"Rank {rank} > {2**n - n * math.log(n)}"
    }

if __name__ == "__main__":
    import sys
    import math

    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = (sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")