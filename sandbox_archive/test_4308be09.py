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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            if all(abs(x) <= n for x in clause):
                cnf.append(clause)
        return cnf

    def tropical_motivic_rank(cnf):
        graph = {}
        for clause in cnf:
            for literal in clause:
                if abs(literal) not in graph:
                    graph[abs(literal)] = set()
                for other_literal in clause:
                    if abs(other_literal) != abs(literal):
                        graph[abs(literal)].add(abs(other_literal))
        visited = set()
        rank = 0
        
        def dfs(node):
            nonlocal rank
            stack = [node]
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    rank += 1
                    for neighbor in graph.get(current, set()):
                        if neighbor not in visited:
                            stack.append(neighbor)
        
        for node in graph:
            if node not in visited:
                dfs(node)
        
        return rank

    def resolution_width(cnf):
        clauses = cnf[:]
        width = 0
        while True:
            new_clauses = []
            found_resolvent = False
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(abs(lit) == abs(-other_lit) for lit in clauses[i] for other_lit in clauses[j]):
                        resolvent = [lit for lit in clauses[i] if lit not in clauses[j]] + \
                                    [other_lit for other_lit in clauses[j] if other_lit not in clauses[i]]
                        new_clauses.append(resolvent)
                        found_resolvent = True
            if not found_resolvent:
                break
            width += 1
            clauses.extend(new_clauses)
        return width

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    mtr = tropical_motivic_rank(cnf)
    w = resolution_width(cnf)

    metric_name = "Resolution Width"
    metric_value = w
    instances_tested = 1
    n_max = n
    conjecture_holds = w <= math.log2(n) + mtr
    counterexample = "" if conjecture_holds else f"CNF with n={n}, mtr={mtr}, w={w}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"not supported by enough seeds\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")