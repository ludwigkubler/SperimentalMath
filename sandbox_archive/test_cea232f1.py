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
            literals = [random.choice([f'x{i}', f'-x{i}']) for i in range(1, n+1)]
            clause = ' | '.join(literals)
            clauses.append(clause)
        return ' & '.join(clauses)
    
    def term_overlap_graph(cnf):
        n = len(cnf.split(' & '))
        graph = [[0] * n for _ in range(n)]
        for i, clause1 in enumerate(cnf.split(' & ')):
            for j, clause2 in enumerate(cnf.split(' & '), start=i+1):
                overlap = sum(1 for lit1 in clause1.split(' | ') if any(lit1 == lit2 or f'-{lit1}' == lit2 for lit2 in clause2.split(' | ')))
                graph[i][j] = overlap
                graph[j][i] = overlap
        return graph
    
    def cholesky_decomposition(matrix):
        n = len(matrix)
        L = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1):
                s = sum(L[i][k] * L[j][k] for k in range(j))
                if i == j:
                    L[i][j] = math.sqrt(matrix[i][i] - s)
                else:
                    L[i][j] = (matrix[i][j] - s) / L[j][j]
        return L
    
    def minimal_index(graph):
        n = len(graph)
        matrix = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                matrix[i][j] = graph[i][j] / (i + 1) ** 0.5
                matrix[j][i] = matrix[i][j]
        L = cholesky_decomposition(matrix)
        index = sum(sum(abs(l)) for l in L) / n
        return index
    
    def is_satisfiable(cnf):
        stack = []
        literals = set()
        for clause in cnf.split(' & '):
            unsatisfied = True
            for literal in clause.split(' | '):
                if literal[0] == '-':
                    if literal[1:] in literals:
                        unsatisfied = False
                        break
                else:
                    if literal not in literals:
                        stack.append(literal)
                        literals.add(literal)
                        unsatisfied = False
                        break
            if unsatisfied:
                while stack and stack[-1] != literal:
                    literals.remove(stack.pop())
        return len(literals) == 0
    
    def sat_complexity(cnf):
        # Simple DPLL solver for demonstration purposes
        n = len(cnf.split(' & '))
        assignment = [False] * (n + 1)
        
        def dpll():
            if all(assignment[i] or not assignment[-i-1] for i in range(1, n+1)):
                return True
            var = next(i for i in range(1, n+1) if not assignment[i] and not assignment[-i-1])
            assignment[var] = True
            if dpll():
                return True
            assignment[var] = False
            assignment[-var-1] = True
            if dpll():
                return True
            return False
        
        return 1 if dpll() else float('inf')
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        graph = term_overlap_graph(cnf)
        index = minimal_index(graph)
        satisfiable = is_satisfiable(cnf)
        complexity = sat_complexity(cnf)
        
        if satisfiable and index > (math.log2(n)) ** 0.25:
            counterexample = f"n={n}, CNF={cnf}, Index={index}, Complexity={complexity}"
            return {
                "metric_name": "Minimal Index",
                "metric_value": index,
                "instances_tested": n_values.count(n),
                "n_max": max(n_values),
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        elif not satisfiable and index <= (math.log2(n)) ** 0.25:
            counterexample = f"n={n}, CNF={cnf}, Index={index}, Complexity={complexity}"
            return {
                "metric_name": "Minimal Index",
                "metric_value": index,
                "instances_tested": n_values.count(n),
                "n_max": max(n_values),
                "conjecture_holds": False,
                "counterexample": counterexample
            }
    
    return {
        "metric_name": "Minimal Index",
        "metric_value": sum(results) / len(results),
        "instances_tested": n_values.count(n),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_d = sum(results) / len(results)
    std_d = math.sqrt(sum((x - mean_d) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= (math.log2(max(n_values))) ** 0.25) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif any(r > (math.log2(max(n_values))) ** 0.25 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > (math.log2(max(n_values))) ** 0.25)
        print(f"RESULT: FALSIFIED counterexample=\"n={max(n_values)}, Index>=(log_2 n)^{1/4}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")