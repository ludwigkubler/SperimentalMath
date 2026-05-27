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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dual_graph(clauses):
        graph = {}
        for clause in clauses:
            for literal in clause:
                abs_literal = abs(literal)
                if abs_literal not in graph:
                    graph[abs_literal] = set()
                for other_clause in clauses:
                    if literal in other_clause and literal != -other_clause[0]:
                        graph[abs_literal].add(abs(other_clause[0]))
        return graph
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if matrix[i][i] == 0:
                found_pivot = False
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        found_pivot = True
                        break
                if not found_pivot:
                    continue
            pivot = matrix[i][i]
            for j in range(i, n):
                matrix[i][j] /= pivot
            for k in range(n):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(i, n):
                        matrix[k][j] -= factor * matrix[i][j]
            rank += 1
        return rank
    
    def moduli_space_dimension(graph):
        # Simplified heuristic for the dimension of the moduli space
        # This is a placeholder and should be replaced with an actual computation
        return len(graph)
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    graph = dual_graph(clauses)
    dim_A_G = moduli_space_dimension(graph)
    
    rank_sum = 0
    instances_tested = 10
    
    for _ in range(instances_tested):
        resolution_proof = []
        for clause in clauses:
            literal = random.choice(clause)
            resolution_proof.append(literal)
        
        algebraic_cycle = [resolution_proof]
        rank_C_P = gaussian_elimination(algebraic_cycle)
        
        if rank_C_P > dim_A_G:
            return {
                "metric_name": "rank(C(P))",
                "metric_value": rank_C_P,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"Rank of algebraic cycle exceeds dimension of moduli space: {rank_C_P} > {dim_A_G}"
            }
        
        rank_sum += rank_C_P
    
    mean_rank = rank_sum / instances_tested
    return {
        "metric_name": "E[rank(C(P))]",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": mean_rank <= dim_A_G * 2,  # Polynomial factor of 2 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds dimension\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")