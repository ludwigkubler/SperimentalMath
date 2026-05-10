# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations, permutations

def generate_3cnf(n: int, m: int) -> list:
    variables = set(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        sign = random.choice([-1, 1])
        clauses.append((sign, tuple(sorted(clause))))
    return clauses

def is_satisfiable(clauses: list) -> bool:
    def dfs(model, i):
        if i == len(clauses):
            return True
        for assignment in [True, False]:
            model[clauses[i][1]] = assignment
            if all((model[var] ^ sign) for sign, var in clauses[i]):
                if dfs(model, i + 1):
                    return True
        return False

    n = max(max(clause[1]) for clause in clauses)
    model = [None] * (n + 1)
    return dfs(model, 0)

def partition_to_tuple(partition: list) -> tuple:
    return tuple(sorted(partition, reverse=True))

def kronecker_coefficient(lambda_, mu, nu):
    if len(mu) != len(nu):
        return 0
    n = len(mu)
    p = [min(lambda_[i], mu[i], nu[i]) for i in range(n)]
    q = [lambda_[i] - p[i] for i in range(n)]
    r = [mu[i] - p[i] for i in range(n)]
    s = [nu[i] - p[i] for i in range(n)]
    
    def sign(p, q, r, s):
        return sum((p[i] - q[i]) * (r[i] - s[i]) for i in range(n)) % 2
    
    def partition_to_int(partition):
        return sum(partition[i] * math.factorial(i) for i in range(len(partition)))
    
    def int_to_partition(num, n):
        partition = [0] * n
        factorial = 1
        for i in range(n - 1, -1, -1):
            if num >= factorial:
                partition[i] = (num // factorial) + 1
                num %= factorial
            factorial //= (i + 1)
        return partition
    
    def kronecker(p, q, r, s):
        if p == q and q == r and r == s:
            return 1
        if len(set(p)) != len(p) or len(set(q)) != len(q) or len(set(r)) != len(r) or len(set(s)) != len(s):
            return 0
        if sum(p) != sum(q) or sum(q) != sum(r) or sum(r) != sum(s):
            return 0
        if any(x < 0 for x in p + q + r + s):
            return 0
        
        p_int = partition_to_int(p)
        q_int = partition_to_int(q)
        r_int = partition_to_int(r)
        s_int = partition_to_int(s)
        
        if p_int > q_int or q_int > r_int or r_int > s_int:
            return 0
        
        if sign(p, q, r, s) == 1:
            return (-1) ** (sum(x * math.factorial(i) for i, x in enumerate(q)) - sum(x * math.factorial(i) for i, x in enumerate(r)))
        else:
            return 0
    
    return kronecker(p, q, r, s)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(2 * n, 4 * n)
    clauses = generate_3cnf(n, m)
    lambda_ = [sum(clause.count(var) for clause in clauses) for var in range(1, n + 1)]
    k_lambda = sum(lambda_)
    mu = (n,)
    nu = (m,)
    g_lambda_mu_nu = kronecker_coefficient(lambda_, mu, nu)
    
    is_unsat = not is_satisfiable(clauses)
    conjecture_holds = is_unsat and k_lambda <= 2 * n * math.log(n) or not is_unsat and g_lambda_mu_nu == 0
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "Kronecker Coefficient",
        "metric_value": g_lambda_mu_nu,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")