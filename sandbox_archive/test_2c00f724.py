# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def generate_3_regular_graph(n):
    if n % 2 != 0:
        raise ValueError("n must be even for a 3-regular graph")
    edges = []
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(0, n, 2):
        edges.append((vertices[i], vertices[i+1]))
    random.shuffle(edges)
    for i in range(0, n, 2):
        edges.append((edges[i][0], edges[i+1][0]))
    random.shuffle(edges)
    return edges

def generate_odd_sum_charge(n):
    charge = [random.choice([-1, 1]) for _ in range(n)]
    if sum(charge) % 2 == 0:
        charge[0] *= -1
    return charge

def matching_polynomial(edges, n):
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    dp = [[0] * (1 << n) for _ in range(n)]
    for mask in range(1 << n):
        for u in range(n):
            if mask & (1 << u):
                continue
            dp[u][mask] = 1
            for v in adj[u]:
                if mask & (1 << v):
                    continue
                dp[u][mask] += dp[v][mask | (1 << u)]
    poly = [0] * (n + 1)
    for u in range(n):
        for mask in range(1 << n):
            if mask & (1 << u):
                continue
            poly[bin(mask).count('1')] += dp[u][mask]
    return poly

def mahler_measure(poly):
    roots = []
    for i in range(1, len(poly)):
        if poly[i] != 0:
            roots.append(abs(poly[i]))
    if not roots:
        return 1.0
    product = 1.0
    for r in roots:
        product *= r
    return product

def encode_tseitin_cnf(edges, charge):
    cnf = []
    for u, v in edges:
        cnf.append([u, v, -(len(charge) + len(edges))])
        cnf.append([-u, -v, -(len(charge) + len(edges))])
    for i in range(len(charge)):
        cnf.append([i, -(len(charge) + len(edges))])
    return cnf

def dpll_solver(cnf, var_order):
    assignment = {}
    def unit_propagate():
        changed = True
        while changed:
            changed = False
            for clause in cnf:
                unassigned = [lit for lit in clause if abs(lit) not in assignment]
                if len(unassigned) == 1:
                    lit = unassigned[0]
                    assignment[abs(lit)] = lit > 0
                    changed = True
    def backtrack():
        nonlocal nodes
        nodes += 1
        if all(any(assignment.get(abs(lit), False) == (lit > 0) for lit in clause) for clause in cnf):
            return True
        for var in var_order:
            if var not in assignment:
                for val in [True, False]:
                    assignment[var] = val
                    if backtrack():
                        return True
                    del assignment[var]
                return False
        return False
    nodes = 0
    backtrack()
    return nodes

def run_trial(seed):
    random.seed(seed)
    n = random.choice([8, 10, 12, 14, 16])
    edges = generate_3_regular_graph(n)
    charge = generate_odd_sum_charge(n)
    poly = matching_polynomial(edges, n)
    M = mahler_measure(poly)
    cnf = encode_tseitin_cnf(edges, charge)
    var_orders = [random.sample(range(1, n + 1), n) for _ in range(10)]
    T_values = []
    for var_order in var_orders:
        T = dpll_solver(cnf, var_order)
        T_values.append(T)
    T_median = sorted(T_values)[len(T_values) // 2]
    conjecture_holds = T_median >= M / 2
    counterexample = ""
    if not conjecture_holds:
        counterexample = f"n={n}, T={T_median}, M={M}"
    return {
        "metric_name": "log2_T_minus_log2_M",
        "metric_value": math.log2(T_median) - math.log2(M),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_counts = 0
    counterexamples = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        if result["counterexample"]:
            counterexamples.append(result["counterexample"])
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_counts / len(seeds)
    if counterexamples:
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={seeds[counterexamples.index(counterexamples[0])]}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")