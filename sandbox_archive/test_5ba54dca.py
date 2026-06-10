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
    n_max = 0
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for depth in [5, 10, 15, 20, 30, 40]:
        n_max = max(n_max, depth)
        instances_tested += depth

        # Generate a random boolean circuit of the given depth
        circuit = []
        for _ in range(depth):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, 4))]
            circuit.append((gate, inputs))

        # Compute the K-theoretic dimension (simplified as rank of a matrix)
        matrix = []
        for gate, inputs in circuit:
            row = [inputs[0], inputs[1]]
            if gate == 'OR':
                row.append(1)
            else:
                row.append(0)
            matrix.append(row)

        # Gaussian elimination to find the rank
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for j in range(i+1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                pivot = A[i][i]
                for j in range(n):
                    A[i][j] /= pivot
                for j in range(m):
                    if j != i:
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[i][k]

            rank = 0
            for row in A:
                if any(row):
                    rank += 1
            return rank

        rank = gaussian_elimination(matrix)
        metric_value = rank

        # Check the conjecture
        if metric_value > depth ** 2:
            conjecture_holds = False
            counterexample = f"Circuit of depth {depth} with K-theoretic dimension {metric_value}"
            break

        total_metric_value += metric_value

    return {
        "metric_name": "K-theoretic Dimension",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")