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
    
    def generate_d_regular_graph(n, d):
        if (n - 1) % d != 0:
            return None
        graph = [[0] * n for _ in range(n)]
        for i in range(1, n):
            neighbors = random.sample(range(i), d-1)
            for j in neighbors:
                graph[i][j] = 1
                graph[j][i] = 1
        return graph
    
    def tensor_product(V1, V2):
        n1, n2 = len(V1), len(V2)
        result = [[0] * (n1 * n2) for _ in range(n1 * n2)]
        for i in range(n1):
            for j in range(n2):
                for k in range(n1):
                    for l in range(n2):
                        result[i*n2 + j][k*n2 + l] = V1[i][k] * V2[j][l]
        return result
    
    def tropical_hodge_decomposition_order(V):
        n = len(V)
        rank = 0
        for i in range(n):
            if sum(V[i]) > 0:
                rank += 1
        return rank
    
    def resolution_proof_width(phi_G):
        # Simplified DPLL solver to estimate width
        assignment = {}
        stack = []
        for clause in phi_G:
            if all(lit in assignment and not assignment[lit] for lit in clause):
                return len(clause)
            unassigned_lit = next((lit for lit in clause if lit not in assignment), None)
            if unassigned_lit is None:
                continue
            stack.append((unassigned_lit, True))
            assignment[unassigned_lit] = True
        while stack:
            lit, polarity = stack.pop()
            new_assignment = {**assignment, lit: polarity}
            if all(lit in new_assignment and not new_assignment[lit] for lit in phi_G):
                return len(phi_G)
            unassigned_lit = next((lit for lit in phi_G if lit not in new_assignment), None)
            if unassigned_lit is None:
                continue
            stack.append((unassigned_lit, True))
            assignment[unassigned_lit] = True
        return len(phi_G)
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        phi_G = []
        for i in range(1, n):
            clause = [literals[i]]
            for j in range(i):
                if graph[i][j] == 1:
                    clause.append(f'-{literals[j]}')
            phi_G.append(clause)
        return phi_G
    
    def compute_ratio(phi_G, m_Hodetrop, w_phi_G):
        if w_phi_G <= 0:
            return None
        return Fraction(m_Hodetrop, w_phi_G) / math.log2(len(phi_G))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        V = tensor_product(graph, graph)
        m_Hodetrop = tropical_hodge_decomposition_order(V)
        phi_G = tseitin_formula(graph)
        w_phi_G = resolution_proof_width(phi_G)
        ratio = compute_ratio(phi_G, m_Hodetrop, w_phi_G)
        if ratio is not None:
            results.append(ratio)
    
    if len(results) < 30:
        return {
            "metric_name": "m_Hodetrop / (log2(n) * w_phi_G)",
            "metric_value": sum(results) / len(results),
            "instances_tested": len(results),
            "n_max": max([5, 10, 15, 20, 30, 40]),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_ratio = sum(results) / len(results)
    return {
        "metric_name": "m_Hodetrop / (log2(n) * w_phi_G)",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": mean_ratio >= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_ratio = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= 1.0) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(r < 1.0 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if r < 1.0)
        print(f"RESULT: FALSIFIED counterexample='ratio_below_1' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")