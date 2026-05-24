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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_primes(min_n=5, max_n=40):
        primes = []
        num = 2
        while len(primes) < max_n and num <= 10**6:
            if is_prime(num):
                primes.append(num)
            num += 1
        return random.sample(primes, min(max_n, len(primes)))
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 ** n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i + 1, n)):
                clauses.append(clause)
        return clauses
    
    def clause_indicator_polynomial(clauses):
        n = len(clauses[0])
        poly = [[0] * (2 ** n) for _ in range(2 ** n)]
        for i in range(2 ** n):
            for j in range(2 ** n):
                product = 1
                for k in range(n):
                    if clauses[k][i & (1 << k)] == -clauses[k][j & (1 << k)]:
                        product *= -1
                poly[i][j] = product
        return poly
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[j][i] != 0 for j in range(i, m)):
                rank += 1
                for j in range(n):
                    matrix[i][j], matrix[m - 1][j] = matrix[m - 1][j], matrix[i][j]
                for k in range(m):
                    if k != i and any(matrix[k][j] != 0 for j in range(i, n)):
                        factor = Fraction(matrix[k][i], matrix[i][i])
                        for j in range(n):
                            matrix[k][j] -= factor * matrix[i][j]
        return rank
    
    def dpll_length(clauses):
        stack = []
        assignment = [None] * len(clauses[0])
        
        def backtrack():
            while stack:
                i, val = stack.pop()
                if val == 1:
                    assignment[i] = -1
                else:
                    assignment[i] = 1
                for j in range(len(clauses)):
                    if clauses[j][i] * assignment[i] < 0:
                        break
                else:
                    return True
                stack.append((i, 3 - val))
            return False
        
        def simplify():
            while True:
                changed = False
                for i in range(len(clauses)):
                    if sum(1 for j in range(len(clauses[0])) if clauses[i][j] != 0) == 1:
                        val = next(j for j in range(len(clauses[0])) if clauses[i][j] != 0)
                        assignment[val - 1] = 1
                        changed = True
                    elif sum(1 for j in range(len(clauses[0])) if clauses[i][j] != 0) == -1:
                        val = next(j for j in range(len(clauses[0])) if clauses[i][j] != 0)
                        assignment[val - 1] = -1
                        changed = True
                if not changed:
                    break
            return changed
        
        stack.append((0, 1))
        while stack:
            i, val = stack.pop()
            if val == 2:
                continue
            assignment[i] = val
            if simplify():
                continue
            if backtrack():
                return len(stack)
            stack.append((i, 3 - val))
        
        return len(stack)
    
    def spearman_correlation(x, y):
        n = len(x)
        rank_x = {x[i]: i for i in range(n)}
        rank_y = {y[i]: i for i in range(n)}
        sum_d1_squared = sum((rank_x[x[i]] - rank_y[y[i]]) ** 2 for i in range(n))
        return 1 - (6 * sum_d1_squared) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_3cnf(n)
        poly = clause_indicator_polynomial(clauses)
        min_rank_value = min_rank(poly)
        dpll_length_value = dpll_length(clauses)
        results.append((min_rank_value, dpll_length_value))
    
    if not results:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    x, y = zip(*results)
    rho = spearman_correlation(x, y)
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho > 0.5 and abs(rho) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes()
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")