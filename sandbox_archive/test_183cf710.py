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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(x) != abs(y) for x, y in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        n = len(cnf[0])
        clauses = set(tuple(sorted(c)) for c in cnf)
        queue = list(clauses)
        seen = set(queue)
        
        while queue:
            literal = random.choice([p for clause in queue for p in clause if p > 0])
            new_clauses = []
            for clause in queue:
                if -literal in clause:
                    continue
                new_clause = [p for p in clause if p != literal]
                if not new_clause:
                    return len(queue)
                new_clause.sort()
                if tuple(new_clause) not in seen:
                    seen.add(tuple(new_clause))
                    new_clauses.append(new_clause)
            queue.extend(new_clauses)
        
        return len(queue)
    
    def quantum_logic_rank(cnf):
        n = len(cnf[0])
        matrix = [[Fraction(1, 2)] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for p in clause:
                if p > 0:
                    matrix[p - 1][n] += Fraction(1, len(clause))
                else:
                    matrix[-p - 1][n] -= Fraction(1, len(clause))
        
        for i in range(n):
            if matrix[i][i] == 0:
                return None
            for j in range(n + 1):
                matrix[i][j] /= matrix[i][i]
            for k in range(n + 1):
                if k != i and matrix[k][i] != 0:
                    factor = -matrix[k][i]
                    for j in range(n + 1):
                        matrix[k][j] += factor * matrix[i][j]
        
        rank = n
        for i in range(n, -1, -1):
            if all(matrix[j][i] == 0 for j in range(n + 1)):
                rank -= 1
        
        return rank
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = generate_cnf(n)
        rank = quantum_logic_rank(cnf)
        width = resolution_width(cnf)
        
        if rank is not None:
            results.append((rank, width))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    ranks, widths = zip(*results)
    mean_rank = sum(ranks) / len(ranks)
    mean_width = sum(widths) / len(widths)
    correlation_coefficient = sum((r - mean_rank) * (w - mean_width) for r, w in results) / (len(results) * math.sqrt(sum((r - mean_rank)**2 for r in ranks)) * math.sqrt(sum((w - mean_width)**2 for w in widths)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(correlation_coefficient >= 0.5 for _, _ in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    total_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        total_results.append(result)
    
    mean_value = sum(r["metric_value"] for r in total_results if r["metric_value"] is not None) / len(total_results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in total_results if r["metric_value"] is not None)) / len(total_results)
    support_fraction = sum(1 for r in total_results if r["conjecture_holds"]) / len(total_results)
    
    if all(r["conjecture_holds"] for r in total_results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in total_results) and any(r["metric_value"] >= 0.5 for r in total_results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={seeds[total_results.index(next(r for r in total_results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")