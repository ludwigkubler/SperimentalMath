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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                if j != i:
                    factor = matrix[j][i] / pivot
                    for k in range(n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank

    def boolean_circuit_weight(poly, n):
        # Simplified example of a boolean circuit weight calculation
        # This is just a placeholder and should be replaced with actual logic
        return len(poly) * n

    def generate_generalized_polynomial(n):
        # Placeholder for generating a generalized polynomial
        # This is just a placeholder and should be replaced with actual logic
        return [random.randint(0, 1) for _ in range(n)]

    def rank_in_grothendieck_witt_ring(poly):
        # Placeholder for computing the rank in the Grothendieck-Witt ring
        # This is just a placeholder and should be replaced with actual logic
        return len(poly)

    n = random.randint(5, 40)
    poly = generate_generalized_polynomial(n)
    rho_f = rank_in_grothendieck_witt_ring(poly)
    circuit_weight = boolean_circuit_weight(poly, n)

    if rho_f == 0:
        return {
            "metric_name": "Rank vs Circuit Weight",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

    diff = abs(rho_f - circuit_weight)
    if diff <= 3:
        return {
            "metric_name": "Rank vs Circuit Weight",
            "metric_value": rho_f,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Rank vs Circuit Weight",
            "metric_value": rho_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rho(f)={rho_f}, circuit_weight={circuit_weight}"
        }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")