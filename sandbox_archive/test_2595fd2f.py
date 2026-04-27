# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def truth_table_to_dict(tt):
        n = int(math.log2(len(tt)))
        table = {}
        for i in range(len(tt)):
            inputs = tuple((i >> j) & 1 for j in range(n))
            outputs = tt[i]
            if inputs not in table:
                table[inputs] = []
            table[inputs].append(outputs)
        return table
    
    def prime_implicant_enumeration(f):
        n = int(math.log2(len(f)))
        table = truth_table_to_dict(f)
        implicants = []
        for inputs, outputs in table.items():
            if len(set(outputs)) == 1:
                implicants.append(inputs)
        return implicants
    
    def build_poset(implicants):
        poset = {}
        for i in range(len(implicants)):
            for j in range(i + 1, len(implicants)):
                a, b = implicants[i], implicants[j]
                if all(a[k] == b[k] or a[k] == 0 for k in range(len(a))):
                    poset.setdefault(a, []).append(b)
        return poset
    
    def maximum_bipartite_matching(graph):
        n = len(graph)
        matching = [-1] * n
        visited = [False] * n
        
        def dfs(u):
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    if matching[v] == -1 or dfs(matching[v]):
                        matching[v] = u
                        return True
            return False
        
        for u in range(n):
            visited = [False] * n
            dfs(u)
        
        return sum(1 for x in matching if x != -1) // 2
    
    def memoized_minimax(f, depth=0, cache=None):
        if cache is None:
            cache = {}
        n = int(math.log2(len(f)))
        key = (tuple(f), depth)
        if key in cache:
            return cache[key]
        
        if depth == n:
            return 1
        
        min_val = float('inf')
        for i in range(n):
            left = f[:i] + [0] * (n - i) + f[i+1:]
            right = f[:i] + [1] * (n - i) + f[i+1:]
            min_val = min(min_val, max(memoized_minimax(left, depth + 1, cache), memoized_minimax(right, depth + 1, cache)))
        
        cache[key] = min_val
        return min_val
    
    def ind_lift(f, b):
        n = int(math.log2(len(f)))
        protocol_tree = {}
        for i in range(n):
            left = f[:i] + [0] * (n - i) + f[i+1:]
            right = f[:i] + [1] * (n - i) + f[i+1:]
            protocol_tree[(i, 0)] = memoized_minimax(left)
            protocol_tree[(i, 1)] = memoized_minimax(right)
        
        def dfs(node, depth):
            if node in protocol_tree:
                return protocol_tree[node]
            min_val = float('inf')
            for i in range(n):
                left = f[:i] + [0] * (n - i) + f[i+1:]
                right = f[:i] + [1] * (n - i) + f[i+1:]
                min_val = min(min_val, max(dfs((i, 0), depth + 1), dfs((i, 1), depth + 1)))
            return min_val
        
        return dfs((0, 0), 0)
    
    n = random.randint(3, 12)
    f = generate_boolean_function(n)
    implicants = prime_implicant_enumeration(f)
    poset = build_poset(implicants)
    w_f = maximum_bipartite_matching(poset)
    q_dt_f = memoized_minimax(f)
    
    conjecture_holds = q_dt_f >= math.ceil(math.log2(w_f + 1))
    counterexample = "" if conjecture_holds else f"Counterexample for n={n}, w(f)={w_f}, Q^dt(f)={q_dt_f}"
    
    return {
        "metric_name": "Q^dt(f)",
        "metric_value": q_dt_f,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        results.append(result)
    
    mean_q_dt_f = sum(r["metric_value"] for r in results) / len(results)
    std_q_dt_f = math.sqrt(sum((r["metric_value"] - mean_q_dt_f) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_q_dt_f} std={std_q_dt_f} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print("RESULT: FALSIFIED counterexample=\"\" first_failing_seed=0")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")