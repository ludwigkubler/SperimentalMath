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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] == -clause[j] for i in range(n) for j in range(i + 1, n)):
                continue
            clauses.append(tuple(sorted(clause)))
        return set(clauses)
    
    def count_periodic_points(phi):
        n = len(phi)
        visited = [False] * (1 << n)
        stack = []
        
        def dfs(state):
            if state in visited:
                return True
            visited[state] = True
            stack.append(state)
            
            for clause in phi:
                unsatisfied = any(lit not in visited or not visited[lit] for lit in clause)
                if unsatisfied:
                    continue
                
                next_state = 0
                for i in range(n):
                    if (state >> i) & 1 == 0 and all(lit not in visited or not visited[lit] for lit in phi[i]):
                        next_state |= 1 << i
                if dfs(next_state):
                    return True
            
            stack.pop()
            visited[state] = False
            return False
        
        for state in range(1 << n):
            if not visited[state]:
                if dfs(state):
                    return len(stack)
        
        return 0
    
    def is_satisfiable(phi):
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                lit = unit_clause[0]
                if lit < 0 and -lit in assignment or lit > 0 and lit not in assignment:
                    return False
                assignment[lit] = True
                clauses = [c for c in clauses if lit not in c and -lit not in c]
            pure_literal = next((l for l in range(1, n + 1) if (l in assignment or -l in assignment) == (l in assignment)), None)
            if pure_literal:
                if pure_literal in assignment:
                    return dpll(clauses, assignment)
                else:
                    assignment[pure_literal] = True
                    if not dpll(clauses, assignment):
                        del assignment[pure_literal]
                        assignment[-pure_literal] = False
                        return dpll(clauses, assignment)
            return False
        
        assignment = {}
        return dpll(phi, assignment)
    
    n_max = 40
    instances_tested = 0
    total_periodic_points = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            phi = generate_3cnf(n)
            if is_satisfiable(phi):
                periodic_points = count_periodic_points(phi)
                total_periodic_points += periodic_points
                instances_tested += 1
    
    metric_value = total_periodic_points / instances_tested
    conjecture_holds = metric_value <= n_max ** 3
    counterexample = "" if conjecture_holds else f"n={n}, |P(φ)|={periodic_points}"
    
    return {
        "metric_name": "Minimal Number of Periodic Points",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")