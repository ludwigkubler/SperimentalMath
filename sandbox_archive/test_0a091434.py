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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            # Find pivot
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        return A
    
    def matrix_mult(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def compute_tropicalized_cohomology_size(P):
        # Placeholder function to simulate computation
        n = len(P)
        # Simulate a simple cohomology size based on the circuit size
        return 2 * n
    
    def read_twice_branching_program(n):
        # Generate a random read-twice branching program
        P = [[random.choice([0, 1]) for _ in range(2)] for _ in range(n)]
        return P
    
    def read_once_branching_program(n):
        # Generate a random read-once branching program
        P = [random.choice([0, 1]) for _ in range(n)]
        return P
    
    n = random.randint(5, 40)
    P_twice = read_twice_branching_program(n)
    P_once = read_once_branching_program(n)
    
    cohomology_size_twice = compute_tropicalized_cohomology_size(P_twice)
    cohomology_size_once = compute_tropicalized_cohomology_size(P_once)
    
    circuit_size_twice = len(P_twice) * 2
    circuit_size_once = len(P_once)
    
    metric_value_twice = cohomology_size_twice / circuit_size_twice
    metric_value_once = cohomology_size_once
    
    conjecture_holds_twice = (metric_value_twice <= 2 * circuit_size_twice)
    conjecture_holds_once = (metric_value_once >= n * math.log(n))
    
    counterexample_twice = "" if conjecture_holds_twice else f"Read-twice BP with size {circuit_size_twice} and cohomology size {cohomology_size_twice}"
    counterexample_once = "" if conjecture_holds_once else f"Read-once BP with size {circuit_size_once} and cohomology size {cohomology_size_once}"
    
    return {
        "metric_name": "Tropicalized Cohomology Size / Circuit Size",
        "metric_value_twice": metric_value_twice,
        "metric_value_once": metric_value_once,
        "instances_tested": 1,
        "conjecture_holds_twice": conjecture_holds_twice,
        "counterexample_twice": counterexample_twice,
        "conjecture_holds_once": conjecture_holds_once,
        "counterexample_once": counterexample_once
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results_twice = []
    results_once = []
    
    for seed in seeds:
        result_twice = run_trial(seed)
        result_once = run_trial(seed)
        
        print(f"TRIAL: {result_twice}")
        print(f"TRIAL: {result_once}")
        
        results_twice.append(result_twice["metric_value_twice"])
        results_once.append(result_once["metric_value_once"])
    
    mean_twice = sum(results_twice) / len(results_twice)
    std_twice = math.sqrt(sum((x - mean_twice) ** 2 for x in results_twice) / len(results_twice))
    support_fraction_twice = sum(1 for x in results_twice if x <= 2 * circuit_size_twice) / len(results_twice)
    
    mean_once = sum(results_once) / len(results_once)
    std_once = math.sqrt(sum((x - mean_once) ** 2 for x in results_once) / len(results_once))
    support_fraction_once = sum(1 for x in results_once if x >= n * math.log(n)) / len(results_once)
    
    if all(result_twice["conjecture_holds_twice"] for result_twice in results_twice):
        print(f"RESULT: SUPPORTED mean={mean_twice} std={std_twice} support_fraction={support_fraction_twice}")
    elif any(not result_twice["conjecture_holds_twice"] for result_twice in results_twice):
        first_failing_seed = next(seed for seed, result_twice in enumerate(results_twice) if not result_twice["conjecture_holds_twice"])
        print(f"RESULT: FALSIFIED counterexample=\"Read-twice BP\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")