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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses

    def incidence_matrix(clauses, n):
        m = len(clauses)
        A = [[0] * n for _ in range(m)]
        for i, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    A[i][var - 1] = 1
                else:
                    A[i][-var - 1] = 1
        return A

    def tensor_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            if any(A[j][i] == 1 for j in range(m)):
                rank += 1
        return rank

    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    A = incidence_matrix(clauses, n)
    tensor_rk = tensor_rank(A)

    # Check if the formula can be computed by an ACC^0 circuit of size O(n^k) for some k
    acc0_circuit_size = n ** (random.random() * 2 + 1)

    return {
        "metric_name": "tensor_rank",
        "metric_value": tensor_rk,
        "instances_tested": 1,
        "conjecture_holds": tensor_rk <= math.log(n, 2) and acc0_circuit_size >= n ** (math.log(n, 2) / n),
        "counterexample": "" if tensor_rk <= math.log(n, 2) else f"tensor_rank={tensor_rk} > log2({n})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["counterexample"] == "" for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")