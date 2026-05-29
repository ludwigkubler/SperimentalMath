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
    
    def generate_cnf(n, alpha):
        m = int(alpha * n * (n - 1) / 2)
        clauses = set()
        while len(clauses) < m:
            clause = tuple(random.sample(range(1, n + 1), 3))
            if random.choice([True, False]):
                clause = tuple(-x for x in clause)
            clauses.add(clause)
        return clauses
    
    def hodge_rank(cnf):
        n = max(abs(x) for x in cnf)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for c in cnf:
            for i in c:
                if i > 0:
                    A[i][i] += 1
                else:
                    A[-i][-i] += 1
        rank = gaussian_elimination(A)
        return rank
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            if pivot == 0:
                return n  # Matrix is not full rank
            for j in range(i + 1, n):
                factor = matrix[j][i] / pivot
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
        return sum(1 for row in matrix if any(row))
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std(lst, avg):
        return math.sqrt(sum((x - avg) ** 2 for x in lst) / len(lst))
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        alpha = random.uniform(0.1, 0.9)
        cnf = generate_cnf(n, alpha)
        rank = hodge_rank(cnf)
        ranks.append(rank)
    
    avg_rank = mean(ranks)
    std_rank = std(ranks, avg_rank)
    
    return {
        "metric_name": "average_hodge_rank",
        "metric_value": avg_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": avg_rank <= 10 * n_values[-1],  # Example threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    avg_rank = mean([r["metric_value"] for r in results])
    std_rank = std([r["metric_value"] for r in results], avg_rank)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")