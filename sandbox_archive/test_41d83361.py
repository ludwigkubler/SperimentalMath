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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def quantum_representation(f):
        n = int(math.log2(len(f)))
        Q_f = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i ^ j]:
                    Q_f[i][j] = 1
        return Q_f
    
    def entanglement_matrix(Q_f):
        n = int(math.log2(len(Q_f)))
        M_f = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if Q_f[i][j]:
                    M_f[i][j] = 1
        return M_f
    
    def rank(matrix):
        n = len(matrix)
        matrix_copy = [row[:] for row in matrix]
        rank = 0
        for i in range(n):
            if sum(matrix_copy[i]) == 0:
                continue
            pivot_row = matrix_copy[i]
            for j in range(i + 1, n):
                factor = -matrix_copy[j][i] / pivot_row[i]
                for k in range(n):
                    matrix_copy[j][k] += factor * pivot_row[k]
            rank += 1
        return rank
    
    def bp_readtwice_complexity(f):
        n = int(math.log2(len(f)))
        complexity = 0
        for i in range(2**n):
            if f[i]:
                complexity += 1
        return complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_size = 0
    total_complexity = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_random_boolean_function(n)
            Q_f = quantum_representation(f)
            M_f = entanglement_matrix(Q_f)
            size_Q_f = len(Q_f)
            rank_M_f = rank(M_f)
            complexity = bp_readtwice_complexity(f)
            
            total_rank += rank_M_f
            total_size += size_Q_f
            total_complexity += complexity
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    std_deviation = math.sqrt((total_rank**2 - total_rank * mean_rank) / (instances_tested - 1))
    
    conjecture_holds = mean_rank <= math.log(total_size)
    counterexample = "" if conjecture_holds else f"Mean rank {mean_rank} exceeds log(size(Q_f)) by more than 3 std deviations"
    
    return {
        "metric_name": "Mean Rank of Entanglement Matrix",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / (len(results) - 1))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction too low")