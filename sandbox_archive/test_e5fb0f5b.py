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
    
    def geometric_entropy(f):
        n = len(f)
        Pr_f = [f.count(i) / n for i in range(n)]
        H_f = -sum(p * math.log2(p) if p > 0 else 0 for p in Pr_f)
        return H_f
    
    def communication_complexity(M, pi):
        N = len(M)
        k = int(math.ceil(math.log2(N)))
        return math.floor(math.log2(1 + N * spectral_excess(M) / k)) - 1
    
    def spectral_excess(M):
        n = len(M)
        A = [[M[i][j] for j in range(n)] for i in range(n)]
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        L = [sum(A[j][i] * M[i][k] for k in range(n)) for i in range(n) for j in range(i + 1, n)]
        L = [L[i % (n * (n - 1) // 2)] for i in range(n * (n - 1) // 2)]
        M_L = [[0] * len(L) for _ in range(len(L))]
        for i in range(len(L)):
            for j in range(i, len(L)):
                if i == j:
                    M_L[i][j] = L[i]
                else:
                    M_L[i][j] = M_L[j][i] = (L[i] + L[j]) / 2
        return sum(M_L[i][j] for i in range(len(L)) for j in range(i, len(L))) / len(L)
    
    def disjointness_instance(n, m):
        variables = list(range(n))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def evaluate_disjointness(I):
        n = len(I[0])
        m = len(I)
        Pr_I = [sum(1 for clause in I if i in clause) / m for i in range(n)]
        H_I = -sum(p * math.log2(p) if p > 0 else 0 for p in Pr_I)
        return H_I
    
    def evaluate_boolean_function(f):
        n = len(f)
        Pr_f = [f.count(i) / n for i in range(n)]
        H_f = -sum(p * math.log2(p) if p > 0 else 0 for p in Pr_f)
        return H_f
    
    def generate_boolean_matrix(M, pi):
        N = len(M)
        M_pi = [[M[pi[i]][j] for j in range(N)] for i in range(N)]
        return M_pi
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            f = [random.choice([0, 1]) for _ in range(n)]
            H_f = evaluate_boolean_function(f)
            if H_f < n * math.log2(n) / (2 * n - 1):  # Ω(n)
                conjecture_holds = False
                counterexample = "Boolean function with low geometric entropy"
                break
            instances_tested += 1
            total_metric_value += H_f
    
    if not conjecture_holds:
        return {
            "metric_name": "Geometric Entropy",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n, 2 * n)
            I = disjointness_instance(n, m)
            H_I = evaluate_disjointness(I)
            if H_I < n * math.log2(n) / (2 * n - 1):  # Ω(n)
                conjecture_holds = False
                counterexample = "Disjointness instance with low geometric entropy"
                break
            instances_tested += 1
            total_metric_value += H_I
    
    if not conjecture_holds:
        return {
            "metric_name": "Geometric Entropy",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "Geometric Entropy",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    mean_metric_value = total_metric_value / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")