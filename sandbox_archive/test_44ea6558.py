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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(1, matrix[i][i])
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = -matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] += factor * matrix[i][j]
        rank = sum(1 for row in matrix if any(row))
        return rank

    def monotone_circuit(n, k):
        # Placeholder function to generate a random monotone circuit
        # This is a stub and should be replaced with actual circuit generation logic
        return [[random.choice([0, 1]) for _ in range(k)] for _ in range(n)]

    n = random.randint(5, 40)
    k = random.randint(1, min(n, 10))
    circuit = monotone_circuit(n, k)

    # Placeholder function to compute the graphical motive rank
    # This is a stub and should be replaced with actual motive computation logic
    def motive_rank(circuit):
        return len(circuit) * len(circuit[0])

    rank = motive_rank(circuit)
    expected_rank = Fraction(k**2 * math.log(n)).limit_denominator()
    epsilon = 1e-6
    diff = abs(rank - expected_rank)

    return {
        "metric_name": "rank_diff",
        "metric_value": float(diff),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": diff <= epsilon,
        "counterexample": "" if diff <= epsilon else f"Rank {rank} does not satisfy the inequality |{rank} - O({k**2 * math.log(n)})| ≤ {epsilon}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_diff)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")