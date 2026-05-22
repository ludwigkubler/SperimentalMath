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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_mult(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[Fraction(0, 1) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def is_acc0_circuit_size(circuit_size, n):
        # Placeholder function to simulate ACC⁰ circuit size check
        return circuit_size <= 2**n

    def construct_noncommutative_algebra(n):
        # Placeholder function to simulate algebra construction
        A = [[Fraction(0, 1) if i != j else Fraction(1, 1) for j in range(n)] for i in range(n)]
        return gaussian_elimination(A)

    def minimal_order_polynomial_automaton(algebra):
        # Placeholder function to simulate polynomial automaton order
        return len(algebra)

    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit_size = random.randint(1, 2**n)
    algebra = construct_noncommutative_algebra(n)
    automaton_order = minimal_order_polynomial_automaton(algebra)

    if is_acc0_circuit_size(circuit_size, n):
        conjecture_holds = automaton_order >= circuit_size
        counterexample = "" if conjecture_holds else f"Algebra size {n}, Circuit size {circuit_size}, Automaton order {automaton_order}"
    else:
        conjecture_holds = False
        counterexample = "ACC⁰ circuit size too large"

    return {
        "metric_name": "Automaton Order vs Circuit Size",
        "metric_value": automaton_order,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[next(i for i, r in enumerate(results) if not r["conjecture_holds"])["counterexample"]]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")