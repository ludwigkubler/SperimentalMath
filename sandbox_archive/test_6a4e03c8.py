# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def generate_kcnf(n, k):
    clauses = []
    for _ in range(k * n):
        clause = set(random.sample(range(1, n + 1), 2))
        if len(clause) == 2:
            clauses.append(tuple(sorted(clause)))
    return clauses

def incidence_graph(clauses):
    graph = {}
    for i, clause in enumerate(clauses):
        for v in clause:
            if v not in graph:
                graph[v] = set()
            graph[v].add(i)
    return graph

def count_noncrossing_partitions(graph):
    n = len(graph)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    for i in range(1, n + 1):
        dp[i][i] = 1
        for j in range(i - 1, -1, -1):
            dp[j][i] = sum(dp[j][k] * dp[k + 1][i] for k in range(j, i))
    return dp[0][-1]

def dpll(clauses, assignment):
    if not clauses:
        return True
    pure_literal = next((v for v in range(1, n+1) if (v not in assignment and all(v not in c for c in clauses)) or (-v not in assignment and all(-v not in c for c in clauses))), None)
    if pure_literal is None:
        return False
    assignment[pure_literal] = True
    new_clauses = [c for c in clauses if pure_literal not in c]
    if dpll(new_clauses, assignment):
        return True
    assignment.pop(pure_literal)
    assignment[-pure_literal] = True
    new_clauses = [c for c in clauses if -pure_literal not in c]
    return dpll(new_clauses, assignment)

def resolution_proof_entanglement_complexity(clauses):
    n = len(clauses)
    assignment = {}
    return 1 + sum(1 for _ in range(n) if not dpll(clauses, assignment))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    metric_value = []
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clauses = generate_kcnf(n, k=2)
            graph = incidence_graph(clauses)
            mnp_phi = count_noncrossing_partitions(graph)
            e_phi = resolution_proof_entanglement_complexity(clauses)
            if e_phi == 0:
                continue
            instances_tested += 1
            metric_value.append(mnp_phi / e_phi)

    mean_mnp_e = sum(metric_value) / len(metric_value)
    std_dev = math.sqrt(sum((x - mean_mnp_e) ** 2 for x in metric_value) / len(metric_value))
    support_fraction = Fraction(len([x for x in metric_value if abs(x - 1) <= 3 * std_dev]), len(metric_value))

    if support_fraction < Fraction(8, 10):
        conjecture_holds = False
        counterexample = "support_fraction < 8/10"

    return {
        "metric_name": "mnp_e_ratio",
        "metric_value": mean_mnp_e,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]

    mean_mnp_e = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_mnp_e) ** 2 for result in results) / len(results))
    support_fraction = Fraction(len([result for result in results if abs(result["metric_value"] - 1) <= 3 * std_dev]), len(results))

    print(f"RESULT: {'SUPPORTED' if support_fraction >= Fraction(8, 10) else 'FALSIFIED'} mean={mean_mnp_e} std={std_dev} support_fraction={support_fraction}")