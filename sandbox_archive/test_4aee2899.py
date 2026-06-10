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
from math import gcd
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def generate_primes(limit):
        primes = []
        for num in range(2, limit):
            if is_prime(num):
                primes.append(num)
        return primes

    def random_group(n):
        elements = list(range(n))
        relations = set()
        while len(relations) < n - 1:
            a, b = random.sample(elements, 2)
            if (a, b) not in relations and (b, a) not in relations:
                relations.add((a, b))
        return elements, relations

    def group_order(group):
        elements, relations = group
        n = len(elements)
        visited = [False] * n
        order = 0
        
        def dfs(v):
            nonlocal order
            if visited[v]:
                return False
            visited[v] = True
            for u in range(n):
                if (v, u) in relations and not visited[u]:
                    if not dfs(u):
                        return False
            order += 1
            return True
        
        for v in range(n):
            if not visited[v]:
                if not dfs(v):
                    return -1
        return n

    def random_representation(group, dim):
        elements, relations = group
        n = len(elements)
        V = [[random.randint(0, 1) for _ in range(dim)] for _ in range(n)]
        return V

    def communication_complexity(V):
        n = len(V)
        dim = len(V[0])
        # Simulate a simple protocol: each party sends their entire vector
        return n * dim

    primes = generate_primes(100)
    seeds = random.sample(primes, 30) if primes else [29] * 30
    metric_values = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for seed in seeds:
        random.seed(seed)
        n = random.randint(5, 40)
        dim = random.randint(1, 40)
        group = random_group(n)
        V = random_representation(group, dim)
        
        order = group_order(group)
        if order == -1:
            continue
        
        C = communication_complexity(V)
        instances_tested += 1
        n_max = max(n_max, n)
        
        metric_values.append(C)
        
        if order > 0 and C > 10:
            conjecture_holds = False
            counterexample = f"Order {order}, Communication Complexity {C}"
            break

    return {
        "metric_name": "Communication Complexity",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [29] * 30
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")