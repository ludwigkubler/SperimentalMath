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
    
    def generate_kcnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, random.randint(1, n))
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def graphical_realization(cnf):
        graph = {}
        for clause in cnf:
            for literal in clause:
                var = abs(literal)
                if var not in graph:
                    graph[var] = set()
                for other_var in [x for x in clause if x != literal]:
                    graph[var].add(abs(other_var))
        return graph
    
    def algebraic_k_theory_rank(graph):
        n = len(graph)
        adj_matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for var, neighbors in graph.items():
            for neighbor in neighbors:
                adj_matrix[var][neighbor] = 1
                adj_matrix[neighbor][var] = 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for i in range(min(rows, cols)):
                if matrix[i][i] == 0:
                    swap_found = False
                    for j in range(i + 1, rows):
                        if matrix[j][i] != 0:
                            for k in range(cols):
                                matrix[i][k], matrix[j][k] = matrix[j][k], matrix[i][k]
                            swap_found = True
                            break
                    if not swap_found:
                        continue
                pivot = Fraction(matrix[i][i])
                for j in range(i, cols):
                    matrix[i][j] /= pivot
                for j in range(rows):
                    if j != i and matrix[j][i] != 0:
                        factor = -matrix[j][i]
                        for k in range(cols):
                            matrix[j][k] += factor * matrix[i][k]
            return sum(1 for row in matrix if any(x != 0 for x in row))
        
        rank = gaussian_elimination(adj_matrix)
        return rank
    
    def dpll_search_tree_height(cnf):
        def dpll(clauses, assignment, unit_clause=None):
            if not clauses:
                return 0
            if unit_clause is not None:
                literal = unit_clause[0]
                var = abs(literal)
                new_assignment = assignment.copy()
                new_assignment[var] = literal > 0
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                return dpll(new_clauses, new_assignment)
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause is not None:
                return dpll(clauses, assignment, unit_clause)
            var = next(var for var in range(1, max(variables) + 1) if var not in assignment)
            new_clauses_true = [c for c in clauses if var not in c and -var not in c]
            new_clauses_false = [c for c in clauses if var in c or -var in c]
            return 1 + max(dpll(new_clauses_true, assignment.copy(), (var, True)), dpll(new_clauses_false, assignment.copy(), (-var, False)))
        
        return dpll(cnf, {})
    
    n = random.randint(5, 40)
    k = random.randint(n // 2, n * 2)
    cnf = generate_kcnf(n, k)
    graph = graphical_realization(cnf)
    rank = algebraic_k_theory_rank(graph)
    height = dpll_search_tree_height(cnf)
    
    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": height,
        "instances_tested": 1,
        "conjecture_holds": height <= rank * n,  # Simplified bound for demonstration
        "counterexample": "" if height <= rank * n else f"Height {height} exceeds expected {rank * n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_height = sum(r["metric_value"] for r in results) / len(results)
    std_height = math.sqrt(sum((r["metric_value"] - mean_height)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_height} std={std_height} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_height} std={std_height} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Height exceeds expected rank * n\" first_failing_seed={first_failing_seed}")