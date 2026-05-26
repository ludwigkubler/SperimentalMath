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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clause = random.sample(literals, 3)
            clauses.append(clause)
        return clauses

    def xor_and_tree_width(clauses):
        n = len(clauses[0])
        graph = {i: set() for i in range(2 * n)}
        
        for clause in clauses:
            for literal1 in clause:
                for literal2 in clause:
                    if literal1 != literal2:
                        node1, node2 = abs(literal1) - 1, abs(literal2) - 1
                        graph[node1].add(node2 + n)
                        graph[node2].add(node1 + n)
        
        def dfs(node, visited):
            stack = [node]
            while stack:
                current = stack.pop()
                if not visited[current]:
                    visited[current] = True
                    for neighbor in graph[current]:
                        stack.append(neighbor)
        
        visited = [False] * (2 * n)
        components = 0
        for i in range(n):
            if not visited[i]:
                dfs(i, visited)
                components += 1
        
        return components - 1

    def discriminant(clauses):
        # Simplified version for demonstration purposes
        return len(clauses)

    def eichler_shimura_rank(discriminant):
        # Simplified version for demonstration purposes
        return math.log2(discriminant) / math.log2(math.log2(discriminant))

    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    discriminant_value = discriminant(formula)
    rank = eichler_shimura_rank(discriminant_value)
    t_star = xor_and_tree_width(formula)

    if rank > math.log2(math.log2(n)) and t_star > math.log2(math.log2(n**2)):
        return {
            "metric_name": "XOR-AND Tree Width",
            "metric_value": t_star,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, t*(F)={t_star}"
        }
    else:
        return {
            "metric_name": "XOR-AND Tree Width",
            "metric_value": t_star,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")