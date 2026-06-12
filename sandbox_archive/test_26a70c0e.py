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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0 or n < d + 1:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    if (i, j) not in edges and (j, i) not in edges:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges.add((i, j))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(f'~{literals[j]}')
            clauses.append(clause)
        for i in range(n):
            for j in range(i + 1, n):
                clause1 = [f'~{literals[i]}', f'{literals[j]}']
                clause2 = [f'~{literals[j]}', f'{literals[i]}']
                clauses.append(clause1)
                clauses.append(clause2)
        return literals, clauses
    
    def dpll_solver(literals, clauses):
        n = len(literals)
        assignment = {lit: None for lit in literals}
        
        def solve():
            if all(assignment[lit] is not None for lit in literals):
                if all(all(assignment[lit] == (lit[0] == '~') ^ any(clause[i] == lit for i in range(len(clause))) for clause in clauses) for lit in literals):
                    return True
                else:
                    return False
            
            literal = next(lit for lit in literals if assignment[lit] is None)
            assignment[literal] = True
            if solve():
                return True
            assignment[literal] = False
            if solve():
                return True
            return False
        
        if not solve():
            return None
        
        proof_size = 0
        for lit in literals:
            if assignment[lit]:
                proof_size += len([cl for cl in clauses if any(clause[i] == lit for i in range(len(clause)))])
            else:
                proof_size += len([cl for cl in clauses if any(clause[i] == f'~{lit}' for i in range(len(clause)))])
        return proof_size
    
    def mls(graph):
        n = len(graph)
        max_rank = 0
        for i in range(n):
            rank = sum(1 for j in graph[i] if j > i)
            max_rank = max(max_rank, rank)
        return max_rank
    
    d_values = [3, 4, 5, 6, 7, 8, 9, 10]
    instances_tested = 0
    total_mls = 0
    total_psat = 0
    n_max = 0
    
    for d in d_values:
        for _ in range(30):
            graph = generate_d_regular_graph(d, random.randint(5, 40))
            if graph is None:
                continue
            literals, clauses = tseitin_formula(graph)
            psat = dpll_solver(literals, clauses)
            if psat is None:
                continue
            mls_value = mls(graph)
            instances_tested += 1
            total_mls += mls_value
            total_psat += psat
            n_max = max(n_max, len(graph))
    
    mean_mls = total_mls / instances_tested if instances_tested > 0 else 0
    mean_psat = total_psat / instances_tested if instances_tested > 0 else 0
    
    conjecture_holds = all(mls_value >= 0.75 * psat for mls_value, psat in zip([mean_mls] * instances_tested, [mean_psat] * instances_tested))
    
    return {
        "metric_name": "mls(G)",
        "metric_value": mean_mls,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mls = sum(r["metric_value"] for r in results) / len(results)
    std_mls = math.sqrt(sum((r["metric_value"] - mean_mls) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_mls} std={std_mls} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")