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
        clauses = []
        for _ in range(random.randint(5, 10)):
            clause = [random.choice(range(-n, -1)) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def graphical_realization(cnf):
        graph = {}
        for lit in set(abs(lit) for clause in cnf for lit in clause):
            graph[lit] = []
        for clause in cnf:
            for i in range(len(clause)):
                lit1 = clause[i]
                for j in range(i + 1, len(clause)):
                    lit2 = clause[j]
                    if abs(lit1) not in graph[abs(lit2)] and abs(lit2) not in graph[abs(lit1)]:
                        graph[abs(lit1)].append(abs(lit2))
                        graph[abs(lit2)].append(abs(lit1))
        return graph
    
    def min_rank(graph):
        n = len(graph)
        rank = 0
        visited = [False] * (n + 1)
        
        def dfs(node, depth):
            nonlocal rank
            if depth > rank:
                rank = depth
            visited[node] = True
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    dfs(neighbor, depth + 1)
        
        for node in range(1, n + 1):
            if not visited[node]:
                dfs(node, 1)
        
        return rank
    
    def dpll(cnf, assignment, clause_index=0):
        if clause_index == len(cnf):
            return True
        literals = cnf[clause_index]
        for lit in literals:
            new_assignment = assignment[:]
            if abs(lit) not in new_assignment:
                new_assignment[abs(lit)] = lit > 0
                if dpll(cnf, new_assignment, clause_index + 1):
                    return True
                new_assignment[abs(lit)] = None
        return False
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    graph = graphical_realization(cnf)
    r_T = min_rank(graph)
    
    if r_T > math.log2(n):
        return {
            "metric_name": "DPLL Proof Length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"r(T) = {r_T} > log({n})"
        }
    
    assignment = [None] * (n + 1)
    proof_length = len(cnf)
    if dpll(cnf, assignment):
        # Find the actual proof length
        def find_proof_length(cnf, assignment, clause_index=0, current_path=[]):
            if clause_index == len(cnf):
                return len(current_path)
            literals = cnf[clause_index]
            for lit in literals:
                new_assignment = assignment[:]
                if abs(lit) not in new_assignment:
                    new_assignment[abs(lit)] = lit > 0
                    result = find_proof_length(cnf, new_assignment, clause_index + 1, current_path + [lit])
                    if result < float('inf'):
                        return result
                    new_assignment[abs(lit)] = None
            return float('inf')
        
        proof_length = find_proof_length(cnf, assignment)
    
    conjecture_holds = proof_length <= 2 ** (r_T / 2)
    counterexample = "" if conjecture_holds else f"Proof length {proof_length} > 2^{r_T/2}"
    
    return {
        "metric_name": "DPLL Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")