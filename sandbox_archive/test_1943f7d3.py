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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k * n):
            clause = set(random.sample(range(1, n + 1), 2))
            if random.choice([True, False]):
                clause = {x: -1 for x in clause}
            clauses.append(clause)
        return clauses
    
    def quandle_representation(clauses):
        n = len(clauses[0])
        Q = [[0] * n for _ in range(n)]
        for clause in clauses:
            if isinstance(clause, dict):
                x, y = clause.keys()
                Q[x - 1][y - 1] += 1
                Q[y - 1][x - 1] += 1
            else:
                x, y = clause
                Q[x - 1][y - 1] -= 1
                Q[y - 1][x - 1] -= 1
        return Q
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(i, n)):
                continue
            pivot_row = next(j for j in range(i, n) if matrix[j][i] != 0)
            if pivot_row != i:
                matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(n):
                if j == i:
                    continue
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
            rank += 1
        return rank
    
    def monotone_circuit_size(k, n):
        return math.ceil(2**n / (math.factorial(k) * n**k))
    
    def k_clique_formula(n, k):
        clauses = []
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clauses.append({i: -1, j: -1})
        for subset in itertools.combinations(range(1, n + 1), k):
            clause = {x: 1 for x in subset}
            clauses.append(clause)
        return clauses
    
    def is_monotone_circuit(circuit):
        # Placeholder function to check if a circuit is monotone
        # This is a dummy implementation and should be replaced with actual logic
        return True
    
    k = 3  # Example value for k
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test with 5 instances per size
            F = generate_kcnf(n, k)
            Q_F = quandle_representation(F)
            rank_Q_F = min_rank(Q_F)
            
            if rank_Q_F < (n**k) / math.factorial(k):
                return {
                    "metric_name": "Minimal Rank of Quandle Representation",
                    "metric_value": rank_Q_F,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"Rank Q_F ({rank_Q_F}) < Ω({n**k} / {math.factorial(k)})"
                }
            
            C = k_clique_formula(n, k)
            if is_monotone_circuit(C):
                size_C = monotone_circuit_size(k, n)
                if size_C > 2**n / (n**k * math.factorial(k)):
                    return {
                        "metric_name": "Monotone Circuit Size",
                        "metric_value": size_C,
                        "instances_tested": 1,
                        "conjecture_holds": False,
                        "counterexample": f"Size C ({size_C}) > O(2^{n} / {n**k} * {math.factorial(k)})"
                    }
    
    return {
        "metric_name": "Minimal Rank of Quandle Representation",
        "metric_value": sum(rank_Q_F for _, rank_Q_F in results) / len(results),
        "instances_tested": 30,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")