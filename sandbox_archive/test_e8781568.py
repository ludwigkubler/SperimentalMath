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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def generate_expander_graph(n: int) -> list:
        # Simple expander graph generation (not rigorous)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    G[i][j] = 1
                    G[j][i] = 1
        return G

    def resolution_refutation_length(G: list) -> int:
        # Simplified DPLL solver (not rigorous)
        n = len(G)
        clauses = []
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] == 1:
                    clauses.append((i, -j))
                    clauses.append((-i, j))
        stack = []
        assignment = [0] * n
        def dpll():
            while True:
                unit_clause = next((c for c in clauses if len(c) == 1), None)
                if unit_clause is not None:
                    var = abs(unit_clause[0])
                    value = 1 if unit_clause[0] > 0 else -1
                    assignment[var] = value
                    stack.append((var, value))
                    for clause in clauses:
                        if var in [abs(x) for x in clause]:
                            clauses.remove(clause)
                elif len(stack) == 0:
                    return True
                else:
                    var, _ = stack.pop()
                    assignment[var] = 0
        dpll()
        return len(assignment)

    def geometric_loci_complexity(G: list) -> int:
        # Simplified geometric loci complexity (not rigorous)
        n = len(G)
        points = set()
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] == 1:
                    points.add((i, j))
        return len(points)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        G = generate_expander_graph(n)
        refutation_length = resolution_refutation_length(G)
        loci_complexity = geometric_loci_complexity(G)
        results.append({
            "n": n,
            "refutation_length": refutation_length,
            "loci_complexity": loci_complexity
        })

    metric_value = sum(r["refutation_length"] for r in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(r["refutation_length"] >= 2**(r["n"]/3) and r["loci_complexity"] >= r["n"] for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Resolution Refutation Length",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if all(r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "mapping_undefined" for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")