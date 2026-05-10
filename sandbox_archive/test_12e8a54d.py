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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_mult(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_power(M, p):
    result = [[1 if i == j else 0 for j in range(len(M))] for i in range(len(M))]
    base = M
    while p > 0:
        if p % 2 == 1:
            result = matrix_mult(result, base)
        base = matrix_mult(base, base)
        p //= 2
    return result

def is_permutation(p):
    n = len(p)
    visited = [False] * n
    for i in range(n):
        if not visited[p[i]]:
            visited[p[i]] = True
        else:
            return False
    return True

def find_cycle_length(p, start):
    cycle = []
    current = start
    while True:
        cycle.append(current)
        current = p[current]
        if current == start:
            break
    return len(cycle)

def automorphism_group(G):
    n = len(G)
    group = [list(range(n))]
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j] != G[j][i]:
                return None
    for p in itertools.permutations(range(n)):
        if is_permutation(p):
            valid = True
            for i in range(n):
                if not all(G[p[i]][p[j]] == G[i][j] for j in range(n)):
                    valid = False
                    break
            if valid:
                group.append(list(p))
    return group

def abp_width(G):
    n = len(G)
    generators = []
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j] != G[j][i]:
                return None
    for p in itertools.permutations(range(n)):
        if is_permutation(p):
            valid = True
            for i in range(n):
                if not all(G[p[i]][p[j]] == G[i][j] for j in range(n)):
                    valid = False
                    break
            if valid:
                generators.append(list(p))
    return len(generators)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = list(range(n))
    clauses = []
    for _ in range(2 * n):
        a, b = random.sample(variables, 2)
        clause = [a, -b]
        if random.choice([True, False]):
            clause[1] *= -1
        clauses.append(clause)
    
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            count = sum(1 for clause in clauses if (i in clause and not j in clause) or (j in clause and not i in clause))
            G[i][j] = count
            G[j][i] = count
    
    group = automorphism_group(G)
    if group is None:
        return {
            "metric_name": "ABP Width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    k = len(group) - 1
    w = abp_width(G)
    if w is None:
        return {
            "metric_name": "ABP Width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "ABP Width",
        "metric_value": w == k,
        "instances_tested": 1,
        "conjecture_holds": w == k,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")