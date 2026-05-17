# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def generate_3cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        clause = [random.choice([-x, x]) for x in clause]
        clauses.append(clause)
    return clauses

def is_unsatisfiable(clauses):
    def dpll(clauses, assignment):
        if not clauses:
            return False
        for clause in clauses:
            if all(lit in assignment for lit in clause):
                return False
        for clause in clauses:
            if all(-lit in assignment for lit in clause):
                continue
            for lit in clause:
                if -lit not in assignment:
                    new_assignment = assignment.copy()
                    new_assignment.add(lit)
                    if dpll([c for c in clauses if c != clause], new_assignment):
                        return True
        return False
    return not dpll(clauses, set())

def build_clause_overlap_graph(clauses):
    graph = {}
    for i, clause1 in enumerate(clauses):
        graph[i] = set()
        for j, clause2 in enumerate(clauses):
            if i != j and any(abs(lit1) == abs(lit2) for lit1 in clause1 for lit2 in clause2):
                graph[i].add(j)
    return graph

def compute_fixed_point(graph):
    m = len(graph)
    mu = [Fraction(1, 1) for _ in range(m)]
    for _ in range(500):
        new_mu = [Fraction(1, 1) for _ in range(m)]
        for v in range(m):
            denom = Fraction(1, 1)
            for u in graph[v]:
                denom += mu[u]
            new_mu[v] = Fraction(1, denom)
        if all(abs(new_mu[v] - mu[v]) < Fraction(1, 10**9) for v in range(m)):
            break
        mu = new_mu
    return mu

def compute_lambda(mu):
    return -sum(math.log2(float(mu_v)) for mu_v in mu)

def count_dpll_leaves(clauses, assignment):
    if not clauses:
        return 1
    for clause in clauses:
        if all(lit in assignment for lit in clause):
            return 0
    for clause in clauses:
        if all(-lit in assignment for lit in clause):
            continue
        for lit in clause:
            if -lit not in assignment:
                new_assignment = assignment.copy()
                new_assignment.add(lit)
                leaves = count_dpll_leaves([c for c in clauses if c != clause], new_assignment)
                if leaves > 0:
                    return leaves
    return 0

def run_trial(seed):
    random.seed(seed)
    n_sizes = [10, 14, 18, 22, 26, 30, 34]
    alpha = 4.26
    results = []
    for n in n_sizes:
        m = int(alpha * n)
        while True:
            clauses = generate_3cnf(n, m)
            if is_unsatisfiable(clauses):
                break
        graph = build_clause_overlap_graph(clauses)
        mu = compute_fixed_point(graph)
        Lambda = compute_lambda(mu)
        t_star = count_dpll_leaves(clauses, set())
        r = math.log2(t_star) / Lambda if Lambda > 0 else float('inf')
        results.append(r)
    metric_value = sum(results) / len(results)
    min_r = min(results)
    conjecture_holds = min_r >= 0.125
    counterexample = "" if conjecture_holds else f"r(F) = {min_r} < 0.125"
    return {
        "metric_name": "r(F)",
        "metric_value": metric_value,
        "instances_tested": len(results),
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
        print(f"RESULT: FALSIFIED counterexample=\"{counterexamples[0]}\" first_failing_seed={seeds[counterexamples.index(counterexamples[0])]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")