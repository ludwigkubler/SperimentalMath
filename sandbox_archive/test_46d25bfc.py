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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def graphical_realization(cnf):
        graph = {}
        for clause in cnf:
            for lit in clause:
                if abs(lit) not in graph:
                    graph[abs(lit)] = set()
                for other_lit in clause:
                    if other_lit != lit and abs(other_lit) not in graph[lit]:
                        graph[lit].add(abs(other_lit))
        return graph
    
    def min_rank(graph):
        visited = {node: False for node in graph}
        
        def dfs(node, color):
            stack = [(node, color)]
            while stack:
                current, c = stack.pop()
                if not visited[current]:
                    visited[current] = True
                    for neighbor in graph[current]:
                        if not visited[neighbor]:
                            stack.append((neighbor, -c))
                        elif visited[neighbor] and c == visited[neighbor]:
                            return False
            return True
        
        rank = 0
        while any(not visited[node] for node in graph):
            component = [node for node in graph if not visited[node]]
            if dfs(component[0], 1):
                rank += 1
            else:
                return float('inf')
        return rank
    
    def dpll(cnf, assignment={}):
        unsatisfied = [clause for clause in cnf if all(lit not in assignment or assignment[lit] != (lit > 0) for lit in clause)]
        if not unsatisfied:
            return True
        unit_clause = next((clause for clause in unsatisfied if len(clause) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = (literal > 0)
            if dpll(cnf, new_assignment):
                return True
            else:
                new_assignment[literal] = not (literal > 0)
                if dpll(cnf, new_assignment):
                    return True
                else:
                    return False
        pure_literal = next((lit for lit in range(1, max(abs(lit) for clause in cnf) + 1) if all(lit not in clause or assignment[lit] != (lit > 0) for clause in cnf) and -lit not in assignment), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll(cnf, new_assignment):
                return True
            else:
                new_assignment[pure_literal] = False
                if dpll(cnf, new_assignment):
                    return True
                else:
                    return False
        polarized_clauses = {True: [], False: []}
        for clause in unsatisfied:
            pos_count = sum(1 for lit in clause if lit > 0 and lit not in assignment)
            neg_count = sum(1 for lit in clause if lit < 0 and -lit not in assignment)
            polarized_clauses[pos_count >= neg_count].append(clause)
        if polarized_clauses[True]:
            return dpll(polarized_clauses[True], assignment)
        elif polarized_clauses[False]:
            return dpll(polarized_clauses[False], assignment)
        else:
            return False
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    graph = graphical_realization(cnf)
    r_T = min_rank(graph)
    
    if r_T == float('inf'):
        return {
            "metric_name": "DPLL Proof Length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    proof_length = dpll(cnf)
    
    return {
        "metric_name": "DPLL Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": proof_length <= 2 ** (r_T / 2),
        "counterexample": "" if proof_length <= 2 ** (r_T / 2) else f"Proof length {proof_length} exceeds bound 2^{r_T/2}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient statistical support or budget exceeded")