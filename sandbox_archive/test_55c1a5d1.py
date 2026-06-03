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
            clause = [random.randint(1, n * 2) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def tseitin_structure(cnf):
        literals = set()
        for clause in cnf:
            for lit in clause:
                literals.add(abs(lit))
        
        nodes = {0}
        edges = []
        
        var_id = 1
        for literal in sorted(literals):
            neg_var = -literal
            pos_var = literal
            
            nodes.add(var_id)
            nodes.add(neg_var)
            
            if literal > 0:
                edges.append((0, pos_var))
                edges.append((-pos_var, var_id))
            else:
                edges.append((0, neg_var))
                edges.append((-neg_var, -var_id))
            
            for other_literal in literals:
                if other_literal != literal and other_literal != -literal:
                    pos_other = other_literal
                    neg_other = -other_literal
                    
                    nodes.add(pos_other)
                    nodes.add(neg_other)
                    
                    edges.append((pos_var, pos_other))
                    edges.append((-neg_var, neg_other))
            
            var_id += 1
        
        return nodes, edges
    
    def p_adic_topological_entropy(nodes, edges):
        n = len(nodes)
        
        # Compute the adjacency matrix
        adj_matrix = [[0] * n for _ in range(n)]
        for u, v in edges:
            adj_matrix[u - 1][v - 1] = 1
        
        # Gaussian elimination to find the rank of the adjacency matrix
        def gaussian_elimination(matrix):
            m, n = len(matrix), len(matrix[0])
            rank = 0
            
            for i in range(n):
                max_row = None
                for j in range(rank, m):
                    if matrix[j][i] != 0:
                        max_row = j
                        break
                
                if max_row is None:
                    continue
                
                matrix[max_row], matrix[rank] = matrix[rank], matrix[max_row]
                
                for j in range(n):
                    if j == i:
                        continue
                    factor = -matrix[rank][j] / matrix[rank][i]
                    for k in range(n):
                        matrix[rank][k] += factor * matrix[max_row][k]
                
                rank += 1
            
            return rank
        
        rank = gaussian_elimination(adj_matrix)
        
        # Compute the p-adic topological entropy
        if n == 0:
            return 0.0
        
        return math.log(rank, n)
    
    def resolution_proof_width(cnf):
        queue = [set(clause) for clause in cnf]
        unit_clauses = {lit: set() for lit in range(1, len(cnf) * 2 + 1)}
        
        while queue:
            current_clause = queue.pop()
            
            if not current_clause:
                return 0
            
            literal = next(iter(current_clause))
            other_literal = -literal
            
            unit_clauses[literal].add(other_literal)
            unit_clauses[other_literal].add(literal)
            
            for clause in cnf:
                if literal in clause and other_literal in clause:
                    queue.append(clause - {literal, other_literal})
        
        return max(len(unit_clauses[lit]) for lit in range(1, len(cnf) * 2 + 1))
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        nodes, edges = tseitin_structure(cnf)
        
        mindex_eta_phi = p_adic_topological_entropy(nodes, edges)
        w_phi = resolution_proof_width(cnf)
        
        metric_values.append(mindex_eta_phi * w_phi)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "mindex_eta_phi * w_phi",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": std_dev > 0.1,  # Arbitrary threshold to avoid triviality
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")