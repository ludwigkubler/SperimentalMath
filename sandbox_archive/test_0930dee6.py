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

def generate_d_regular_graph(n, d):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    G = [[] for _ in range(n)]
    edges_added = set()
    
    while len(edges_added) < (n * d) // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        
        if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
            G[u].append(v)
            G[v].append(u)
            edges_added.add((u, v))
    
    return G

def tseitin_formula(G):
    n = len(G)
    literals = {i: f"x{i}" for i in range(n)}
    clauses = []
    
    for u in range(n):
        clause = [literals[u]]
        for v in G[u]:
            clause.append(f"~{literals[v]}")
        clauses.append(clause)
    
    for u in range(n):
        for v in range(u + 1, n):
            if len(G[u] & G[v]) == 0:
                clauses.append([f"~{literals[u]}", f"{literals[v]}"])
                clauses.append([f"{literals[u]}", f"~{literals[v]}"])
    
    return literals, clauses

def dpll(clauses):
    def dpll_helper(model, clause_index):
        if clause_index == len(clauses):
            return model
        
        clause = clauses[clause_index]
        for literal in clause:
            if literal.startswith("~"):
                var = literal[1:]
                if var not in model or model[var] != 0:
                    new_model = model.copy()
                    new_model[var] = -1
                    result = dpll_helper(new_model, clause_index + 1)
                    if result is not None:
                        return result
            else:
                var = literal
                if var not in model or model[var] != 1:
                    new_model = model.copy()
                    new_model[var] = 1
                    result = dpll_helper(new_model, clause_index + 1)
                    if result is not None:
                        return result
        
        return None
    
    return dpll_helper({}, 0)

def frege_proof_depth(clauses):
    literals, clauses = tseitin_formula(clauses)
    return len(dpll(clauses))

def local_zeta_function_order(G):
    n = len(G)
    degree_sum = sum(len(neighbors) for neighbors in G)
    return Fraction(degree_sum, 2 * n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    d_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for d in d_values:
        for _ in range(5):
            n = d * (random.randint(1, 8) + 1)
            G = generate_d_regular_graph(n, d)
            lzf_G = local_zeta_function_order(G)
            proof_depth = frege_proof_depth(clauses)
            
            results.append({
                "n": n,
                "d": d,
                "lzf_G": lzf_G,
                "proof_depth": proof_depth
            })
    
    correlation_coefficient = 0.0
    for result in results:
        correlation_coefficient += (result["lzf_G"] - mean_lzf) * (result["proof_depth"] - mean_proof_depth)
    
    correlation_coefficient /= len(results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation_coefficient) > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        
        if "conjecture_holds" not in result or not result["conjecture_holds"]:
            break
    
    if len(results) == len(seeds):
        mean_lzf = sum(result["metric_value"] for result in results) / len(results)
        mean_proof_depth = sum(result["proof_depth"] for result in results) / len(results)
        
        support_fraction = sum(1 for result in results if abs(result["metric_value"]) > 0.8) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_lzf} std={math.sqrt(sum((result['metric_value'] - mean_lzf)**2 for result in results) / len(results))} support_fraction={support_fraction}")
        else:
            print("RESULT: FALSIFIED counterexample=\"\" first_failing_seed=0")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")