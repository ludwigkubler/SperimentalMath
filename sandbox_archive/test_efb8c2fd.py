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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [variables[i]]
            for j in range(i+1, n):
                clause.append(f'~{variables[j]}')
            clauses.append(clause)
        return variables, clauses
    
    def generate_quasigroup(size):
        if size == 2:
            return [[0, 1], [1, 0]]
        q = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append((i + j) % size)
            q.append(row)
        return q
    
    def is_valid_quasigroup(q, clauses):
        n = len(q)
        variables = [f'x{i}' for i in range(n)]
        assignments = {}
        
        def assign(var, val):
            if var not in assignments:
                assignments[var] = val
        
        def evaluate_clause(clause):
            return any(assignments[var] == val for var, val in zip(clause, [0, 1]))
        
        def backtrack(i):
            if i == n:
                return all(evaluate_clause(clause) for clause in clauses)
            for j in range(n):
                assign(variables[i], j)
                if backtrack(i + 1):
                    return True
                del assignments[variables[i]]
            return False
        
        return backtrack(0)
    
    def resolution_refutation_depth(q, clauses):
        n = len(q)
        variables = [f'x{i}' for i in range(n)]
        queue = []
        
        def add_clause(clause):
            queue.append(clause)
        
        def resolve(c1, c2):
            new_clause = set()
            for lit in c1:
                if '~' + lit not in c2:
                    new_clause.add(lit)
            return list(new_clause)
        
        def is_tautology(clause):
            return any(lit == '~' + lit for lit in clause)
        
        add_clause([f'~{variables[i]}' for i in range(n)])
        
        while queue:
            c1 = queue.pop(0)
            if is_tautology(c1):
                continue
            for c2 in queue:
                if any(lit == '~' + lit for lit in c2):
                    continue
                new_clause = resolve(c1, c2)
                if not new_clause:
                    return len(queue) + 1
                add_clause(new_clause)
        
        return len(queue)
    
    def quasigroup_rank(q):
        n = len(q)
        rank = 0
        for i in range(n):
            row = q[i]
            col = [q[j][i] for j in range(n)]
            if all(row[k] == col[k] for k in range(n)):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    
    min_rank = float('inf')
    max_depth = 0
    
    for _ in range(30):
        q = generate_quasigroup(2**n)
        if is_valid_quasigroup(q, clauses):
            rank = quasigroup_rank(q)
            depth = resolution_refutation_depth(q, clauses)
            min_rank = min(min_rank, rank)
            max_depth = max(max_depth, depth)
    
    metric_value = max_depth / min_rank
    conjecture_holds = abs(metric_value - min_rank) > math.exp(0.1 * math.log2(n))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Resolution Refutation Depth to Minimal Quasigroup Rank",
        "metric_value": metric_value,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")