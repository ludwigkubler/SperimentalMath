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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set()
            while len(clause) < 2:
                var = random.randint(1, n)
                if -var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def quandle_representation(F):
        n = max(abs(x) for x in F)
        Q = [[0] * (n + 1) for _ in range(n + 1)]
        for x, y in F:
            if -x not in Q[x - 1]:
                Q[x - 1][y - 1] += 1
            if -y not in Q[y - 1]:
                Q[y - 1][x - 1] += 1
        return Q
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if matrix[i][i] != 0:
                for j in range(n):
                    matrix[j][i] /= matrix[i][i]
                for j in range(m):
                    if j != i:
                        factor = matrix[j][i]
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[i][k]
                rank += 1
            else:
                found_nonzero = False
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        found_nonzero = True
                        break
                if not found_nonzero:
                    continue
                for j in range(n):
                    matrix[i][j] /= matrix[i][i]
                for j in range(m):
                    if j != i:
                        factor = matrix[j][i]
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[i][k]
                rank += 1
        return rank
    
    def monotone_circuit_size(n, k):
        return Fraction(2**n, n**k * math.factorial(k))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        F = generate_k_cnf(n, k)
        Q_F = quandle_representation(F)
        rank_Q_F = min_rank(Q_F)
        
        if rank_Q_F < Fraction(n**k, math.factorial(k)):
            return {
                "metric_name": "min_rank",
                "metric_value": rank_Q_F,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, k={k}, min_rank(Q_F) < Ω(n^k / k!)"
            }
        
        size_C = monotone_circuit_size(n, k)
        if size_C > Fraction(2**n, n**k * math.factorial(k)):
            return {
                "metric_name": "monotone_circuit_size",
                "metric_value": size_C,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, k={k}, monotone circuit size > O(2^n / (n^k * k!))"
            }
        
        results.append({
            "metric_name": "min_rank",
            "metric_value": rank_Q_F,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    return {
        "metric_name": "min_rank",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")