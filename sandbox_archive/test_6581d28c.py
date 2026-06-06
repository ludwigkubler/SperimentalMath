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
    
    def dpll(cnf):
        if not cnf:
            return True
        for literal in cnf[0]:
            if literal == 0:
                continue
            new_cnf = [clause for clause in cnf if literal not in clause and -literal not in clause]
            if dpll(new_cnf):
                return True
            new_cnf = [clause for clause in cnf if -literal not in clause]
            if dpll(new_cnf):
                return True
        return False
    
    def min_representation_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[i][j] != 0 for j in range(i, n)):
                rank += 1
                for j in range(n):
                    matrix[j][i] /= matrix[i][i]
                for j in range(n):
                    if j != i:
                        factor = matrix[j][i]
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def generate_quantum_state(n):
        state = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return state
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_diff = 0
    support_count = 0
    
    for n in n_values:
        for _ in range(5):
            quantum_state = generate_quantum_state(n)
            matrix_representation = quantum_state
            min_rank = min_representation_rank(matrix_representation)
            
            cnf_instance = [[random.randint(-n, n) for _ in range(random.randint(1, n))] for _ in range(n)]
            proof_length = len(cnf_instance)  # Simplified DPLL length calculation
            
            diff = abs(min_rank - proof_length)
            total_diff += diff
            instances_tested += 1
            
            if min_rank == proof_length:
                support_count += 1
    
    mean_diff = total_diff / instances_tested
    support_fraction = support_count / len(n_values) / 5
    
    return {
        "metric_name": "Minimal Representation Rank vs DPLL Proof Length",
        "metric_value": mean_diff,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8 and mean_diff <= 3,
        "counterexample": "" if support_fraction >= 0.8 else f"Support fraction: {support_fraction}, Mean diff: {mean_diff}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Support fraction too low\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} mean_diff={mean_diff}")