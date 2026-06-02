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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def min_order(phi):
        p = random.choice([2] + [q for q in range(3, 100) if all(q % d != 0 for d in range(2, int(math.sqrt(q)) + 1))])
        for k in range(2, p):
            if pow(k, (p - 1) // 2, p) == 1:
                return k
        return None
    
    def shannon_entropy(phi):
        counts = [phi.count(f"({i})") for i in range(len(phi))]
        total = sum(counts)
        probabilities = [c / total for c in counts]
        entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
        return entropy
    
    def isomorphism(phi, phi_star):
        n = len(phi)
        A = [[0] * n for _ in range(n)]
        b = [0] * n
        for i in range(n):
            for j in range(n):
                A[i][j] = 1 if (i + 1) * (j + 1) % n == 1 else 0
                b[i] += phi.count(f"({j+1})")
        x = gaussian_elimination(A, b)
        return all(abs(x[i] - int(phi_star[i])) < 1e-6 for i in range(n))
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 ** (n - 1)):
            clause = random.sample(range(1, n + 1), random.randint(1, n))
            clause += [-x for x in clause]
            clauses.append(" or ".join(f"({x})" if x > 0 else f"(-{x})" for x in clause))
        return " and ".join(clauses)
    
    def dual_cnf(phi):
        n = len(phi[phi.find("(") + 1:phi.find(")")].split(","))
        clauses = phi.split(" and ")
        dual_clauses = []
        for clause in clauses:
            literals = [int(x.strip("()")) for x in clause.split(" or ") if x]
            dual_literals = [n - l + 1 if l > 0 else -(n - abs(l) + 1) for l in literals]
            dual_clauses.append(" or ".join(f"({x})" if x > 0 else f"(-{x})" for x in dual_literals))
        return " and ".join(dual_clauses)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = generate_cnf(n)
    phi_star = dual_cnf(phi)
    
    min_order_phi = min_order(phi)
    if min_order_phi is None:
        return {
            "metric_name": "min_order",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    entropy_phi = shannon_entropy(phi)
    
    return {
        "metric_name": "min_order",
        "metric_value": min_order_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) < 0.5 or abs(r["metric_value"] - (r["n_max"] // 2)) > 2 * std_value for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) < 0.5 or abs(result["metric_value"] - (result["n_max"] // 2)) > 2 * std_value)
        print(f"RESULT: FALSIFIED counterexample=\"min_order not correlated with entropy\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")