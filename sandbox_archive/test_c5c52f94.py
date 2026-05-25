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
    
    def generate_tseitin_formula(n, delta):
        variables = list(range(1, n + 1))
        clauses = []
        for var in variables:
            clause = [random.choice([-1, 1]) * var]
            for _ in range(delta - 1):
                other_var = random.choice(variables)
                if other_var != var:
                    clause.append(random.choice([-1, 1]) * other_var)
            clauses.append(clause)
        return variables, clauses
    
    def tseitin_formula_to_graph(variables, clauses):
        n = len(variables)
        graph = {i: set() for i in range(n)}
        for clause in clauses:
            literals = [abs(lit) - 1 for lit in clause]
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    graph[literals[i]].add(literals[j])
                    graph[literals[j]].add(literals[i])
        return graph
    
    def quantum_group_cohomology_rank(graph):
        n = len(graph)
        adj_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                adj_matrix[i][j-1] = 1
                adj_matrix[j-1][i] = 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for i in range(cols):
                if all(matrix[r][i] == 0 for r in range(rank, rows)):
                    continue
                matrix[rank], matrix[i] = matrix[i], matrix[rank]
                for j in range(rows):
                    if j != rank:
                        factor = -matrix[j][i] / matrix[rank][i]
                        for k in range(cols):
                            matrix[j][k] += factor * matrix[rank][k]
                rank += 1
            return rank
        
        return gaussian_elimination(adj_matrix)
    
    def resolution_proof_length(clauses):
        # Simplified DPLL solver to estimate proof length
        stack = []
        assignment = {}
        for var in range(1, len(variables) + 1):
            assignment[var] = None
        def dpll():
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                var, sign = abs(literal), -1 if literal < 0 else 1
                assignment[var] = sign
                stack.append((var, sign))
                new_clauses = []
                for c in clauses:
                    if literal not in c and -literal not in c:
                        new_clauses.append(c)
                if dpll():
                    return True
                stack.pop()
                assignment[var] = None
            else:
                var = next(v for v, a in assignment.items() if a is None)
                assignment[var] = 1
                stack.append((var, 1))
                new_clauses = []
                for c in clauses:
                    if -var in c:
                        return False
                    elif var not in c:
                        new_clauses.append(c)
                if dpll():
                    return True
                stack.pop()
                assignment[var] = -1
                stack.append((var, -1))
                new_clauses = []
                for c in clauses:
                    if var in c:
                        return False
                    elif -var not in c:
                        new_clauses.append(c)
                if dpll():
                    return True
                stack.pop()
            return False
        dpll()
        return len(stack)
    
    n = random.randint(5, 40)
    delta = random.randint(1, 5)
    variables, clauses = generate_tseitin_formula(n, delta)
    graph = tseitin_formula_to_graph(variables, clauses)
    rank = quantum_group_cohomology_rank(graph)
    proof_length = resolution_proof_length(clauses)
    
    lower_bound = 2 ** (math.log2(n / delta) ** 2)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= lower_bound,
        "counterexample": "" if rank >= lower_bound else f"n={n}, delta={delta}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")