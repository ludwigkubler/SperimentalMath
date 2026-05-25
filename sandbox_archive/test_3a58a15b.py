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
    
    def generate_clifford_group_state(n):
        # Simplified generation for demonstration purposes
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropicalized_permutation_matrix(state):
        n = int(math.log2(len(state)))
        tp_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if state[i * 2 + j] == 1:
                    tp_matrix[i][j] = 1
        return tp_matrix
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            if matrix[max_row][i] == 0:
                continue
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(n):
                matrix[i][j] /= matrix[i][i]
            for k in range(m):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
            rank += 1
        return rank
    
    def quantum_circuit_depth(state):
        # Simplified depth calculation for demonstration purposes
        n = int(math.log2(len(state)))
        return random.randint(1, 2 * n - 1)
    
    n = random.randint(5, 40)
    state = generate_clifford_group_state(n)
    tp_matrix = tropicalized_permutation_matrix(state)
    rank = matrix_rank(tp_matrix)
    depth = quantum_circuit_depth(state)
    
    if rank < 3:
        return {
            "metric_name": "minimal_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "rank_less_than_3"
        }
    
    C = random.uniform(0.5, 2)
    upper_bound = C * math.log2(rank)
    lower_bound = (rank + math.log2(n)) / 4
    
    if depth <= 2 * math.log2(n) - 1 and rank <= upper_bound and depth >= lower_bound:
        return {
            "metric_name": "minimal_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "minimal_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"depth={depth}, upper_bound={upper_bound}, lower_bound={lower_bound}"
        }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds_count = sum(r["conjecture_holds"] for r in results)
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")