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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {f'x{i}': i for i in range(n)}
        clauses = []
        
        # Add clauses for each edge
        for u, v in graph:
            x_u = f'x{u}'
            x_v = f'x{v}'
            new_var = f'y{len(literals)}'
            literals[new_var] = len(literals)
            clauses.append([f'-{x_u}', f'-{x_v}', new_var])
            clauses.append([f'{x_u}', f'{new_var}'])
            clauses.append([f'{x_v}', f'{new_var}'])
        
        # Add clauses for each node
        for i in range(n):
            x_i = f'x{i}'
            new_var = f'y{len(literals)}'
            literals[new_var] = len(literals)
            clauses.append([f'-{x_i}', new_var])
            clauses.append([f'{x_i}'])
        
        return literals, clauses
    
    def symplectic_matrix(graph):
        n = len(graph)
        M = [[0 for _ in range(2 * n)] for _ in range(2 * n)]
        
        # Fill the matrix with identity blocks
        for i in range(n):
            M[i][i] = 1
            M[n + i][n + i] = 1
        
        # Fill the matrix with edge information
        for u, v in graph:
            M[u][v + n] = -1
            M[v][u + n] = -1
            M[v + n][u] = 1
            M[u + n][v] = 1
        
        return M
    
    def matrix_rank(M):
        m, n = len(M), len(M[0])
        rank = 0
        for i in range(m):
            if any(M[i][j] != 0 for j in range(n)):
                rank += 1
                for j in range(n):
                    M[i][j] /= M[i][i]
                for k in range(m):
                    if k != i:
                        factor = M[k][i]
                        for j in range(n):
                            M[k][j] -= factor * M[i][j]
        return rank
    
    def resolution_proof_length(clauses):
        # Simplified version of resolution proof length calculation
        return len(clauses)
    
    n = random.randint(5, 40)
    graph = generate_graph(n)
    literals, clauses = tseitin_formula(graph)
    M = symplectic_matrix(graph)
    rank_M = matrix_rank(M)
    proof_length = resolution_proof_length(clauses)
    
    return {
        "metric_name": "Rank of Symplectic Matrix / Resolution Proof Length",
        "metric_value": Fraction(rank_M, proof_length),
        "instances_tested": 1,
        "conjecture_holds": rank_M >= 2 ** (math.ceil(math.log(proof_length, 2))),
        "counterexample": "" if rank_M >= 2 ** (math.ceil(math.log(proof_length, 2))) else f"Graph with n={n} and proof length {proof_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"] and result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support for conjecture found")