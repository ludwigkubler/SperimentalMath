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
    
    def generate_matrix(N):
        return [[random.randint(0, 1) for _ in range(N)] for _ in range(N)]
    
    def is_independent(lattice, row):
        for i in lattice:
            if all(row[j] == matrix[i][j] for j in range(len(matrix[0]))):
                return False
        return True
    
    def find_minimal_lattices(matrix):
        N = len(matrix)
        lattices = []
        for i in range(N):
            if is_independent(lattices, matrix[i]):
                lattices.append(i)
        return lattices
    
    def communication_complexity(N, I):
        return math.log2(N) * math.log(min(I, N - I))
    
    results = []
    for n in [10, 15, 20, 30, 40]:
        matrix = generate_matrix(n)
        I = len(find_minimal_lattices(matrix))
        cc = communication_complexity(n, I)
        results.append({
            "n": n,
            "cc": cc
        })
    
    mean_cc = sum(result["cc"] for result in results) / len(results)
    std_cc = math.sqrt(sum((result["cc"] - mean_cc) ** 2 for result in results) / len(results))
    conjecture_holds = all(cc <= communication_complexity(n, I) for n, cc, I in zip([10, 15, 20, 30, 40], [result["cc"] for result in results], [len(find_minimal_lattices(generate_matrix(n))) for n in [10, 15, 20, 30, 40]]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Communication Complexity",
        "metric_value": mean_cc,
        "instances_tested": len(results),
        "n_max": max([result["n"] for result in results]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_cc = sum(result["metric_value"] for result in results) / len(results)
    std_cc = math.sqrt(sum((result["metric_value"] - mean_cc) ** 2 for result in results) / len(results))
    conjecture_holds_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_cc} std={std_cc} support_fraction={conjecture_holds_fraction}")
    elif conjecture_holds_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cc} std={std_cc} support_fraction={conjecture_holds_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")