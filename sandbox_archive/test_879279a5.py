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
    
    def generate_read_twice_circuit(n):
        if n == 1:
            return [[0]]
        else:
            left = generate_read_twice_circuit(n // 2)
            right = generate_read_twice_circuit(n - n // 2)
            circuit = []
            for i in range(len(left)):
                circuit.append([left[i][0] + right[i][0]])
            return circuit
    
    def symplectic_form_rank(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        m = n // 2
        A = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                A[i][j] = circuit[i][0][j]
        C = [[A[i][j] - A[i+m//2][j+m//2] for j in range(n)] for i in range(m)]
        rank = 0
        for row in C:
            if any(row):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_read_twice_circuit(n)
        rank = symplectic_form_rank(circuit)
        expected_rank = math.log2(n) ** 2
        ratio = rank / expected_rank if expected_rank != 0 else float('inf')
        results.append({
            "n": n,
            "rank": rank,
            "expected_rank": expected_rank,
            "ratio": ratio
        })
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["ratio"] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["ratio"] - 1) < 0.3) / len(results)
    
    return {
        "metric_name": "Ratio of Symplectic Form Rank to Expected Rank",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={results[0]['n']}, rank={results[0]['rank']}, expected_rank={results[0]['expected_rank']}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, rank={results[0]['rank']}, expected_rank={results[0]['expected_rank']}\" first_failing_seed={first_failing_seed}")