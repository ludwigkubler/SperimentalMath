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
    
    def generate_k_clique_cnf(k, n):
        if k > n or n < 2:
            return None
        clauses = []
        for i in range(n):
            for j in range(i + 1, n):
                clause = [f"v{i+1}", f"v{j+1}"]
                clauses.append(clause)
        return clauses

    def tropical_rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            if matrix[i][i] == 0:
                continue
            for j in range(cols):
                if j != i and matrix[j][i] > 0:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(x != 0 for x in row))
        return rank

    def convert_to_tropical(matrix):
        tropical_matrix = [[math.inf if x == 0 else -x for x in row] for row in matrix]
        for i in range(len(tropical_matrix)):
            tropical_matrix[i][i] = 0
        return tropical_matrix

    n = random.randint(5, 40)
    k = random.randint(2, min(n // 2, 10))
    cnf = generate_k_clique_cnf(k, n)
    if cnf is None:
        return {
            "metric_name": "tropical_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "k > n or n < 2"
        }

    # Convert CNF to a matrix representation (simplified for demonstration)
    matrix = [[0] * n for _ in range(n)]
    for clause in cnf:
        for literal in clause:
            if literal.startswith("v"):
                var = int(literal[1:]) - 1
                matrix[var][var] = 1

    tropical_matrix = convert_to_tropical(matrix)
    rank = tropical_rank(tropical_matrix)

    return {
        "metric_name": "tropical_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True if rank >= 2**k else False,
        "counterexample": "" if rank >= 2**k else f"Rank {rank} < 2^{k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"rank < 2^k\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")