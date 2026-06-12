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
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, tuple):
            op = circuit[0]
            left = evaluate_circuit(circuit[1])
            right = evaluate_circuit(circuit[2])
            if op == 'AND':
                return min(left, right)
            elif op == 'OR':
                return max(left, right)
            else:
                raise ValueError(f"Unknown operation: {op}")
        else:
            return circuit
    
    def tropical_hermitian_form(circuit):
        n = len(circuit)
        H = [[0] * n for _ in range(n)]
        
        def assign_values(node, value, n):
            if isinstance(node, tuple):
                op = node[0]
                left = evaluate_circuit(node[1])
                right = evaluate_circuit(node[2])
                if op == 'AND':
                    H[left][right] = max(H[left][right], value)
                    H[right][left] = max(H[right][left], value)
                elif op == 'OR':
                    H[left][right] = max(H[left][right], value)
                    H[right][left] = max(H[right][left], value)
            else:
                node[0] = value
        
        assign_values(circuit, 0, n)
        
        return H
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m == 0 or n == 0:
            return 0
        for i in range(m):
            if matrix[i][i] != 0:
                for j in range(n):
                    if j != i:
                        factor = -matrix[j][i] / matrix[i][i]
                        for k in range(n):
                            matrix[j][k] += factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    depths = [5, 10, 15, 20, 30, 40]
    ranks = []
    instances_tested = 0
    n_max = 0
    
    for depth in depths:
        for _ in range(5):
            circuit = ['AND', (random.choice(['OR', 'AND']), [random.randint(0, depth-1), random.randint(0, depth-1)]), [random.randint(0, depth-1), random.randint(0, depth-1)]]
            H = tropical_hermitian_form(circuit)
            rank_value = rank(H)
            ranks.append(rank_value)
            instances_tested += 1
            n_max = max(n_max, len(circuit))
    
    mean_rank = sum(ranks) / len(ranks)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in ranks) / len(ranks))
    correlation_coefficient = pearson_correlation(depths * 5, ranks)
    
    conjecture_holds = correlation_coefficient >= 0.7 and all(rank_value >= depth / 2 for rank_value, depth in zip(ranks, depths * 5))
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}> avg_rank/depth=<{}>".format(correlation_coefficient, mean_rank / max(depths))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={:.4f} std={:.4f} support_fraction={:.2f}".format(mean_rank, std_rank, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(r["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")