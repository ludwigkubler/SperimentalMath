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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(3)]
            if 0 not in clause:
                clauses.append(clause)
        return clauses
    
    def dual_graph(clauses):
        graph = {}
        for clause in clauses:
            for i in range(3):
                u, v = clause[i], clause[(i + 1) % 3]
                if u not in graph: graph[u] = set()
                if v not in graph: graph[v] = set()
                graph[u].add(v)
                graph[v].add(u)
        return graph
    
    def resolution_proof(clauses):
        stack = []
        while clauses:
            clause1, clause2 = random.sample(clauses, 2)
            new_clause = [x for x in clause1 if x not in clause2 and -x not in clause2]
            if not new_clause:
                return None
            clauses.remove(clause1)
            clauses.remove(clause2)
            clauses.append(new_clause)
        return stack
    
    def algebraic_cycle(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            if graph[i]:
                rank += 1
        return rank
    
    def dim_moduli_space(graph):
        n = len(graph)
        return n - 1
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    G = dual_graph(clauses)
    P = resolution_proof(clauses)
    
    if not P:
        return {
            "metric_name": "rank(C(P))",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_failed"
        }
    
    rank_C_P = algebraic_cycle(G)
    dim_A_G = dim_moduli_space(G)
    
    return {
        "metric_name": "rank(C(P))",
        "metric_value": rank_C_P,
        "instances_tested": 1,
        "conjecture_holds": rank_C_P <= dim_A_G,
        "counterexample": "" if rank_C_P <= dim_A_G else f"rank(C(P))={rank_C_P} > dim(A(G))={dim_A_G}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    elif any("counterexample" in r and r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["conjecture_holds"] is False)
        result = f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE no_data"
    
    print(result)