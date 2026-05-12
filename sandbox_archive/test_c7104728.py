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
from itertools import combinations

def generate_dnf(n: int) -> list:
    dnf = set()
    for i in range(1, n + 1):
        terms = [set() for _ in range(i)]
        for j in range(n):
            if random.choice([True, False]):
                terms[j % i].add(j)
        dnf.add(tuple(sorted(term) for term in terms))
    return list(dnf)

def max_matching_size(dnf: list) -> int:
    n = len(dnf[0])
    adj_matrix = [[0] * n for _ in range(n)]
    for clause in dnf:
        for i in range(n):
            if i not in clause:
                continue
            for j in range(i + 1, n):
                if j not in clause:
                    adj_matrix[i][j] += 1
                    adj_matrix[j][i] += 1
    
    matching = []
    visited = [False] * n
    
    def dfs(u: int) -> bool:
        for v in range(n):
            if adj_matrix[u][v] > 0 and not visited[v]:
                visited[v] = True
                if v not in matching or dfs(matching[v]):
                    matching[v] = u
                    return True
        return False
    
    for i in range(n):
        if not visited[i]:
            dfs(i)
    
    return sum(1 for x in matching if x != -1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    dnf_size = n**2
    k = 3  # Example value for k-CLIQUE
    
    dnf = generate_dnf(n)
    mu_F = max_matching_size(dnf)
    
    if len(dnf[0]) == n:
        mu_F_k_clique = sum(1 for _ in combinations(range(n), k))
    else:
        mu_F_k_clique = -1
    
    metric_name = "mu_F"
    metric_value = mu_F
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if len(dnf[0]) == n:
        if mu_F >= n**(1 - 1/k):
            conjecture_holds = True
        else:
            counterexample = "k-CLIQUE instance does not meet the conjecture"
    elif mu_F <= math.log(n):
        conjecture_holds = True
    else:
        counterexample = "General DNF does not meet the conjecture"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")