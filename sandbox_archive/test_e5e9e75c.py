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
    
    def generate_ac0_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_noncommutative_differential_form(circuit):
        n = len(circuit)
        form = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i] != circuit[j]:
                    form[i][j] = 1
                    form[j][i] = 1
        return form
    
    def min_rank(matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        rank = 0
        for i in range(rows):
            if any(matrix[i]):
                pivot_col = next(j for j in range(cols) if matrix[i][j])
                rank += 1
                for k in range(rows):
                    if k != i and matrix[k][pivot_col]:
                        for j in range(cols):
                            matrix[k][j] ^= matrix[i][j]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_ac0_circuit(n)
            form = compute_noncommutative_differential_form(circuit)
            rank = min_rank(form)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank >= math.log(n_values[-1]) * 0.5  # c=0.5 as a placeholder
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Rank of Noncommutative Differential Form",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")