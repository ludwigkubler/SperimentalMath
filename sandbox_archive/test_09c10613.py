# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            while len(set(clause)) != 2:
                clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def construct_groupoid(clauses):
        G = {}
        for lit in set(abs(lit) for clause in clauses for lit in clause):
            G[lit] = set()
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    lit1, lit2 = clause[i], clause[j]
                    if abs(lit1) != abs(lit2):
                        G[abs(lit1)].add(abs(lit2))
                        G[abs(lit2)].add(abs(lit1))
        return G
    
    def compute_min_homrank(G):
        n = len(G)
        adj_matrix = [[0] * n for _ in range(n)]
        for i, lit1 in enumerate(G):
            for lit2 in G[lit1]:
                adj_matrix[i][G.index(abs(lit2))] = 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            for col in range(cols):
                pivot_row = None
                for row in range(col, rows):
                    if matrix[row][col] != 0:
                        pivot_row = row
                        break
                if pivot_row is None:
                    continue
                for r in range(rows):
                    if r != pivot_row:
                        factor = matrix[r][col] / matrix[pivot_row][col]
                        for c in range(cols):
                            matrix[r][c] -= factor * matrix[pivot_row][c]
            return matrix
        
        reduced_matrix = gaussian_elimination(adj_matrix)
        rank = sum(1 for row in reduced_matrix if any(row))
        return rank
    
    def sat_complexity(cnf):
        # Simplified DPLL solver
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clauses = [c[0] for c in clauses if len(c) == 1]
            if unit_clauses:
                lit = unit_clauses[0]
                new_assignment = assignment.copy()
                new_assignment[lit] = True
                if dpll([c for c in clauses if lit not in c and -lit not in c], new_assignment):
                    return True
                new_assignment[lit] = False
                if dpll([c for c in clauses if -lit not in c], new_assignment):
                    return True
                return False
            pure_lits = []
            for lit in range(1, max(abs(l) for l in itertools.chain.from_iterable(cnf)) + 1):
                pos_count = sum(1 for clause in cnf if lit in clause)
                neg_count = sum(1 for clause in cnf if -lit in clause)
                if pos_count == 0:
                    pure_lits.append(lit)
                elif neg_count == 0:
                    pure_lits.append(-lit)
            if pure_lits:
                lit = pure_lits[0]
                new_assignment = assignment.copy()
                new_assignment[lit] = True
                if dpll([c for c in cnf if lit not in c and -lit not in c], new_assignment):
                    return True
                new_assignment[lit] = False
                if dpll([c for c in cnf if -lit not in c], new_assignment):
                    return True
                return False
            literal, _ = min((len(c), lit) for lit in range(1, max(abs(l) for l in itertools.chain.from_iterable(cnf)) + 1) for c in cnf)
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            new_assignment[-literal] = True
            if dpll([c for c in cnf if -literal not in c], new_assignment):
                return True
            return False
        
        return 1 if dpll(cnf, {}) else float('inf')
    
    n_max = 40
    instances_tested = 30
    metrics = []
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(n, n * 2)
        cnf = generate_cnf(n, m)
        G = construct_groupoid(cnf)
        min_homrank = compute_min_homrank(G)
        sat_complexity_val = sat_complexity(cnf)
        
        if min_homrank == 0:
            continue
        
        metrics.append((min_homrank, sat_complexity_val))
    
    if not metrics:
        return {
            "metric_name": "min_homrank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_homranks, sat_complexity_vals = zip(*metrics)
    correlation_coefficient = sum((x - mean_min_homranks) * (y - mean_sat_complexity_vals) for x, y in zip(min_homranks, sat_complexity_vals)) / (len(metrics) * std_min_homranks * std_sat_complexity_vals)
    
    return {
        "metric_name": "min_homrank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7 and all(corr >= 0.5 for corr in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and all(corr >= 0.5 for corr, r in zip([r["metric_value"] for r in results], results)):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(corr < 0.5 for corr, r in zip([r["metric_value"] for r in results], results)):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_violation\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'] and corr < 0.5)]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")