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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def matrix_representation(clauses):
        n = len(clauses[0])
        m = len(clauses)
        A = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(clauses):
            for j in clause:
                if j > 0:
                    A[i][j - 1] = 1
                else:
                    A[i][-1] += 1
        return A
    
    def tropical_symplectic_volume(A):
        n = len(A[0]) - 1
        m = len(A)
        volume = 0
        for i in range(m):
            max_val = -math.inf
            for j in range(n):
                if A[i][j] > max_val:
                    max_val = A[i][j]
            volume += max_val
        return volume
    
    def entropy(clauses):
        n = len(clauses[0])
        counts = [0] * (n + 1)
        for clause in clauses:
            for j in clause:
                if j > 0:
                    counts[j - 1] += 1
                else:
                    counts[-1] += abs(j)
        total = sum(counts)
        entropy = 0
        for count in counts:
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)
        return entropy
    
    def spearman_correlation(ranks):
        n = len(ranks)
        ranks_x, ranks_y = zip(*ranks)
        x_bar = sum(ranks_x) / n
        y_bar = sum(ranks_y) / n
        numerator = sum((x - x_bar) * (y - y_bar) for x, y in ranks)
        denominator = math.sqrt(sum((x - x_bar)**2 for x in ranks_x)) * math.sqrt(sum((y - y_bar)**2 for y in ranks_y))
        return numerator / denominator
    
    def rank(data):
        sorted_data = sorted(data)
        rank_dict = {value: idx + 1 for idx, value in enumerate(sorted_data)}
        return [(rank_dict[value], value) for value in data]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        clauses = generate_cnf(n)
        A = matrix_representation(clauses)
        tsv = tropical_symplectic_volume(A)
        ent = entropy(clauses)
        results.append((tsv, ent))
    
    ranks_tsv = rank([result[0] for result in results])
    ranks_ent = rank([result[1] for result in results])
    correlation = spearman_correlation(ranks_tsv)
    
    return {
        "metric_name": "Spearman's Rank Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": "" if correlation >= 0.5 else "Spearman's rank correlation coefficient < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and min(r["metric_value"] for r in results if not r["conjecture_holds"]) < 0.5:
        print(f"RESULT: FALSIFIED counterexample='Spearman's rank correlation coefficient < 0.5' first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")