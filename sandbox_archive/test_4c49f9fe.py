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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def smith_normal_form(M):
    n = len(M)
    for k in range(n):
        # Find pivot
        i_max = k
        j_max = k
        for i in range(k, n):
            for j in range(k, n):
                if abs(M[i][j]) > abs(M[i_max][j_max]):
                    i_max, j_max = i, j
        M[k], M[i_max] = M[i_max], M[k]
        M[k][k] //= gcd(M[k][k], M[j_max][k])
        
        # Eliminate below pivot
        for i in range(k + 1, n):
            factor = M[i][k] // M[k][k]
            for j in range(k, n):
                M[i][j] -= factor * M[k][j]
                
        # Eliminate above pivot
        for i in range(k):
            factor = M[i][k] // M[k][k]
            for j in range(k, n):
                M[i][j] -= factor * M[k][j]
    return M

def log2_int(n):
    if n <= 0:
        return -math.inf
    count = 0
    while n > 1:
        n //= 2
        count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_graph(n, is_expander):
        if is_expander:
            # Configuration model for expanders
            G = [[0] * n for _ in range(n)]
            degrees = [3] * n
            while any(d != 3 for d in degrees):
                for i in range(n):
                    if degrees[i] > 0:
                        j = random.choice([j for j in range(n) if j != i and G[i][j] == 0])
                        G[i][j], G[j][i] = 1, 1
                        degrees[i] -= 1
                        degrees[j] -= 1
            return G
        else:
            # Prism graph for non-expanders
            n //= 2
            G = [[0] * (n + n) for _ in range(n + n)]
            for i in range(n):
                G[i][i + n], G[i + n][i] = 1, 1
                G[n - 1 - i][n - 1 - i + n], G[n - 1 - i + n][n - 1 - i] = 1, 1
                for j in range(n):
                    if j != i and j != n - 1 - i:
                        G[i][j], G[j][i] = 1, 1
                        G[n - 1 - i][j + n], G[j + n][n - 1 - i] = 1, 1
            return G
    
    def build_tseitin_formula(G, omega):
        m = len(G)
        n = m // 2
        formula = []
        for v in range(n):
            x = [f"x_{v}_{i}" for i in range(3)]
            formula.append([x[0], x[1], -x[2]])
            formula.append([-x[0], -x[1], x[2]])
            for u, w in enumerate(G[v]):
                if w:
                    formula.append([f"x_{v}_{i}", f"x_{u}_{j}", -omega[u] ^ omega[w]])
        return formula
    
    def dpll(formula):
        n = len(formula)
        assignment = [0] * (n * 3)
        stack = []
        
        def propagate():
            while stack:
                literal, value = stack.pop()
                index = abs(literal) - 1
                if assignment[index] == -value:
                    return False
                elif assignment[index] == 0:
                    assignment[index] = value
                    for clause in formula[index * 3:index * 3 + 3]:
                        if literal not in clause and -literal not in clause:
                            stack.append((clause[0], -assignment[abs(clause[0]) - 1]))
                            stack.append((clause[1], -assignment[abs(clause[1]) - 1]))
                            stack.append((clause[2], -assignment[abs(clause[2]) - 1]))
            return True
        
        def search():
            if not propagate():
                return False
            unassigned = [i for i in range(n * 3) if assignment[i] == 0]
            if not unassigned:
                return True
            literal = unassigned[0]
            value = 1
            stack.append((literal, value))
            if search():
                return True
            stack.pop()
            value = -1
            stack.append((literal, value))
            if search():
                return True
            stack.pop()
            return False
        
        return search(), assignment
    
    n_values = [8, 10, 12, 14, 16, 18, 20]
    results = []
    
    for n in n_values:
        for _ in range(30):
            is_expander = random.choice([True, False])
            G = generate_graph(n, is_expander)
            omega = {v: random.randint(0, 1) for v in range(n)}
            formula = build_tseitin_formula(G, omega)
            decision_nodes, _ = dpll(formula)
            results.append({
                "n": n,
                "is_expander": is_expander,
                "decision_nodes": decision_nodes
            })
    
    log2_t_star = [log2_int(result["decision_nodes"]) for result in results]
    nu_G = [log2_int(max(abs(sum(row)) for row in smith_normal_form(G))) for G, _ in zip(results, n_values)]
    
    r = sum(x * y for x, y in zip(log2_t_star, nu_G)) / (sum(x ** 2 for x in log2_t_star) * sum(y ** 2 for y in nu_G))
    mean_log2_t_star = sum(log2_t_star) / len(log2_t_star)
    mean_nu_G = sum(nu_G) / len(nu_G)
    
    conjecture_holds = r >= 0.6 and all(t >= 0.1 * n - 5 for t, n in zip(log2_t_star, nu_G)) and all(n <= 4 * math.log2(n) for n in nu_G)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "log2_t_star",
        "metric_value": mean_log2_t_star,
        "instances_tested": len(log2_t_star),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_log2_t_star = sum(result["metric_value"] for result in results) / len(results)
    std_log2_t_star = math.sqrt(sum((result["metric_value"] - mean_log2_t_star) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_log2_t_star} std={std_log2_t_star} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")