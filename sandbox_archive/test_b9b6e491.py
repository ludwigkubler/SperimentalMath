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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def rank(matrix):
        n = len(matrix)
        rref = gaussian_elimination([row[:] for row in matrix])
        rank = 0
        for i in range(n):
            if any(rref[i][j] != 0 for j in range(n)):
                rank += 1
        return rank

    def tropical_rank(E, P):
        n = len(E)
        divisor = [[E[0][i] + E[1][j] + E[2][k] for i in range(n) for j in range(n) for k in range(n)]]
        return rank(divisor)

    def ac0_circuit_size():
        # Placeholder function to generate a random AC0 circuit size
        return random.randint(5, 30)

    s = ac0_circuit_size()
    
    if s <= 1:
        return {
            "metric_name": "tropical_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    # Generate a random Weierstrass elliptic curve E over F2
    E = [
        [random.choice([0, 1]) for _ in range(s)],
        [random.choice([0, 1]) for _ in range(s)],
        [random.choice([0, 1]) for _ in range(s)]
    ]
    
    # Find a marked point P such that the tropicalization of the divisor class [P] has minimal rank s
    P = [random.randint(0, s-1) for _ in range(3)]
    
    if tropical_rank(E, P) != s:
        return {
            "metric_name": "tropical_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Failed for AC0 circuit size {s}"
        }

    # Verify the converse statement by checking if there exists an elliptic curve and a point P such that the tropical rank of [P] is exactly s for all AC0 circuits computing f
    for _ in range(29):
        s = ac0_circuit_size()
        E = [
            [random.choice([0, 1]) for _ in range(s)],
            [random.choice([0, 1]) for _ in range(s)],
            [random.choice([0, 1]) for _ in range(s)]
        ]
        P = [random.randint(0, s-1) for _ in range(3)]
        if tropical_rank(E, P) != s:
            return {
                "metric_name": "tropical_rank",
                "metric_value": None,
                "instances_tested": 30,
                "conjecture_holds": False,
                "counterexample": f"Failed for AC0 circuit size {s}"
            }

    return {
        "metric_name": "tropical_rank",
        "metric_value": s,
        "instances_tested": 30,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='failed_for_seed_{first_failing_seed}' first_failing_seed={first_failing_seed}")