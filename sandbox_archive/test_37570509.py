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
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0 or d < 1 or d > n - 1:
            return None
        graph = [[] for _ in range(n)]
        edges_used = set()
        for i in range(d * n // 2):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            while u == v or (u, v) in edges_used or (v, u) in edges_used:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
            graph[u].append(v)
            graph[v].append(u)
            edges_used.add((u, v))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for u in range(n):
            clause = [literals[u]]
            for v in graph[u]:
                clause.append(f'-{literals[v]}')
            clauses.append(clause)
            for v in graph[u]:
                for w in graph[v]:
                    if u != w:
                        clauses.append([f'-{literals[u]}', f'{literals[v]}', f'-{literals[w]}'])
        return literals, clauses
    
    def resolution_proof_width(clauses):
        n = len(clauses)
        variables = set()
        for clause in clauses:
            for literal in clause:
                if literal.startswith('-'):
                    variables.add(literal[1:])
                else:
                    variables.add(literal)
        
        def solve(lits_true, lits_false):
            stack = []
            while True:
                unit_clauses = [c for c in clauses if len(c - lits_true) == 1 and not (c & lits_false)]
                if not unit_clauses:
                    break
                new_lit = unit_clauses[0] - lits_true
                if new_lit in lits_false:
                    return False
                stack.append((new_lit, 'true'))
                lits_true.add(new_lit)
            
            while stack:
                lit, truth = stack.pop()
                if truth == 'true':
                    for clause in clauses:
                        if lit in clause and not (clause - lits_true):
                            new_lit = clause - lits_true
                            if new_lit in lits_false:
                                return False
                            stack.append((new_lit, 'true'))
                            lits_true.add(new_lit)
                else:
                    for clause in clauses:
                        if -lit in clause and not (clause & lits_false):
                            new_lit = -clause - lits_false
                            if new_lit in lits_true:
                                return False
                            stack.append((new_lit, 'false'))
                            lits_false.add(new_lit)
            
            return True
        
        max_width = 0
        for _ in range(100):  # Sample 100 random assignments
            lits_true = set()
            lits_false = set()
            for var in variables:
                if random.choice([True, False]):
                    lits_true.add(var)
                else:
                    lits_false.add(var)
            
            width = len(lits_true) + len(lits_false)
            if not solve(lits_true, lits_false):
                return 0
            max_width = max(max_width, width)
        
        return max_width
    
    def tropical_analytic_rank(clauses):
        n = len(clauses)
        variables = set()
        for clause in clauses:
            for literal in clause:
                if literal.startswith('-'):
                    variables.add(literal[1:])
                else:
                    variables.add(literal)
        
        rank = 0
        for var in variables:
            max_val = -math.inf
            for clause in clauses:
                val = 0
                for lit in clause:
                    if lit == var:
                        val += 1
                    elif lit.startswith('-') and lit[1:] == var:
                        val -= 1
                max_val = max(max_val, val)
            rank += max_val
        
        return rank
    
    n_values = [10, 15, 20, 30, 40]
    ratios = []
    
    for n in n_values:
        for _ in range(6):  # Sample 6 instances per size
            d = random.randint(2, n - 1)
            graph = generate_d_regular_graph(n, d)
            if graph is None:
                continue
            
            literals, clauses = tseitin_formula(graph)
            tar_value = tropical_analytic_rank(clauses)
            w_value = resolution_proof_width(clauses)
            
            if w_value == 0:
                continue
            
            ratios.append(tar_value / w_value)
    
    if not ratios:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((r - mean_ratio) ** 2 for r in ratios) / len(ratios))
    support_fraction = sum(1 for r in ratios if r <= 10) / len(ratios)
    
    return {
        "metric_name": "Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(ratios),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": "" if support_fraction >= 0.95 else f"Ratio {max(ratios)} > 10"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio {max(r['metric_value'] for r in results)} > 10\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")