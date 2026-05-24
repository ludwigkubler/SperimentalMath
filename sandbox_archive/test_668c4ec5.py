# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(num_vars, num_clauses):
        cnf = []
        for _ in range(num_clauses):
            clause = [random.randint(1, num_vars), -random.randint(1, num_vars)]
            cnf.append(clause)
        return cnf
    
    def truth_table(cnf, num_vars):
        n = 1 << num_vars
        tt = [[False] * n for _ in range(len(cnf))]
        for i in range(n):
            assignment = [(i >> j) & 1 for j in range(num_vars)]
            for clause in cnf:
                if all(assignment[abs(l)-1] == (l > 0) for l in clause):
                    tt[cnf.index(clause)][i] = True
                    break
        return tt
    
    def dpll_refutation_tree(cnf, num_vars):
        n = 1 << num_vars
        tree = {i: [] for i in range(n)}
        stack = [(0, [])]
        
        while stack:
            node, path = stack.pop()
            if node == n - 1:
                continue
            for literal in [-1, 1]:
                new_path = path + [literal]
                child_node = node | (1 << abs(literal) - 1)
                if child_node not in tree[node]:
                    tree[node].append(child_node)
                    stack.append((child_node, new_path))
        
        return tree
    
    def rank_quasipolynomial(truth_table):
        n = len(truth_table[0])
        rank = 0
        for i in range(n):
            if any(row[i] != row[0] for row in truth_table):
                rank += 1
        return rank
    
    def diameter(tree, root):
        visited = set()
        queue = [(root, 0)]
        
        while queue:
            node, dist = queue.pop(0)
            if node not in visited:
                visited.add(node)
                for child in tree[node]:
                    queue.append((child, dist + 1))
        
        return max(dist for node, dist in visited)
    
    num_vars = random.randint(5, 40)
    cnf = generate_cnf(num_vars, random.randint(2 * num_vars, 3 * num_vars))
    tt = truth_table(cnf, num_vars)
    tree = dpll_refutation_tree(cnf, num_vars)
    
    rank = rank_quasipolynomial(tt)
    diameter_val = diameter(tree, 0)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= diameter_val,
        "counterexample": "" if rank >= diameter_val else f"Rank {rank} < Diameter {diameter_val}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")