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
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 30
    total_lzf = 0
    total_depth = 0

    for n in n_values:
        for _ in range(instances_tested // len(n_values)):
            d = random.randint(1, min(n - 1, 5))
            G = generate_d_regular_graph(n, d)
            φ_G = construct_tseitin_formula(G)
            lzf_G = compute_local_zeta_function_order(φ_G)
            depth_G = compute_frege_proof_depth(φ_G)

            total_lzf += lzf_G
            total_depth += depth_G

    mean_lzf = Fraction(total_lzf, instances_tested * len(n_values))
    mean_depth = Fraction(total_depth, instances_tested * len(n_values))

    correlation_coefficient = (instances_tested * sum(lzf * depth for lzf, depth in zip([mean_lzf] * instances_tested, [mean_depth] * instances_tested)) - 
                                (instances_tested * mean_lzf * mean_depth)) / (
        math.sqrt(instances_tested * sum((lzf - mean_lzf) ** 2 for lzf in [mean_lzf] * instances_tested)) *
        math.sqrt(instances_tested * sum((depth - mean_depth) ** 2 for depth in [mean_depth] * instances_tested))
    )

    conjecture_holds = abs(correlation_coefficient) >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested * len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_d_regular_graph(n: int, d: int) -> list:
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    G = [[] for _ in range(n)]
    edges_added = set()
    
    def add_edge(u: int, v: int):
        if (u, v) not in edges_added and (v, u) not in edges_added:
            G[u].append(v)
            G[v].append(u)
            edges_added.add((u, v))
            edges_added.add((v, u))

    for i in range(n):
        for j in range(i + 1, n):
            if len(G[i]) < d and len(G[j]) < d:
                add_edge(i, j)

    return G

def construct_tseitin_formula(G: list) -> str:
    n = len(G)
    variables = {i: f"x{i}" for i in range(n)}
    clauses = []

    def literal(v: int, negated: bool):
        return (variables[v], not negated)

    def negate(lit: tuple):
        var, negated = lit
        return (var, not negated)

    def or_clause(*lits: tuple):
        return " ∨ ".join(f"{var}{'!' if negated else ''}" for var, negated in lits)

    def and_clause(*clauses: str):
        return " ∧ ".join(clauses)

    for i in range(n):
        clauses.append(or_clause(literal(i, False), literal(i, True)))

    for i in range(n):
        for j in G[i]:
            clauses.append(or_clause(negate(literal(i, True)), negate(literal(j, True))))
            clauses.append(or_clause(negate(literal(i, False)), negate(literal(j, False))))

    return and_clause(*clauses)

def compute_local_zeta_function_order(φ_G: str) -> Fraction:
    # Placeholder for actual computation
    return Fraction(1, 2)

def compute_frege_proof_depth(φ_G: str) -> Fraction:
    # Placeholder for actual computation
    return Fraction(3, 4)

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2**31 - 1, 2**63 - 1) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported")