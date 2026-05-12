# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import permutations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_planar_graph(n):
        # Simple planar graph generation (not exhaustive)
        if n == 3:
            return [(0, 1), (1, 2), (2, 0)]
        elif n == 4:
            return [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
        else:
            raise ValueError("Unsupported graph size for this simple generator")
    
    def tseitin_formula(graph):
        # Construct Tseitin formula from a planar graph
        n = len(graph)
        literals = [f"x{i}" for i in range(n)]
        clauses = []
        for u, v in graph:
            clauses.append([literals[u], f"~{literals[v]}"])
            clauses.append([f"~{literals[u]}", literals[v]])
        return clauses
    
    def non_abelian_fourier_coefficients(clauses):
        n = len(clauses)
        F = [0] * (2 ** n)
        for perm in permutations(range(n)):
            sign = 1
            for i, clause in enumerate(clauses):
                if all(perm[j] == int(lit[1:]) - 1 for lit in clause if lit[0] != '~'):
                    continue
                elif any(perm[j] == int(lit[1:]) - 1 for lit in clause if lit[0] == '~'):
                    sign *= -1
            F[sum(1 if i == j else 0 for i, j in enumerate(perm))] += sign
        return F
    
    def resolution_length(clauses):
        # Simple DPLL with clause learning (not exhaustive)
        stack = []
        learned_clauses = set()
        while clauses:
            literal = random.choice([c[0] for c in clauses if c[0][0] != '~'] + [f"~{c[0]}" for c in clauses])
            if literal.startswith('~'):
                literal = literal[1:]
                polarity = False
            else:
                polarity = True
            stack.append((literal, polarity))
            while stack:
                lit, pol = stack.pop()
                if lit in learned_clauses:
                    continue
                found = False
                for i, clause in enumerate(clauses):
                    if literal in clause:
                        clauses[i].remove(literal)
                        if not clauses[i]:
                            return 0
                        if polarity != (lit[0] == '~'):
                            stack.extend([(c, True) for c in clauses[i]])
                        else:
                            stack.extend([(c, False) for c in clauses[i]])
                        found = True
                        break
                if not found:
                    learned_clauses.add(lit)
        return len(learned_clauses)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = generate_planar_graph(n)
    clauses = tseitin_formula(graph)
    F = non_abelian_fourier_coefficients(clauses)
    coefficient_spread = max(abs(x) for x in F) - min(abs(x) for x in F)
    proof_length = resolution_length(clauses)
    
    if coefficient_spread * proof_length == 0:
        return {
            "metric_name": "spread_times_proof_length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    expected = math.sqrt(n)
    ratio = coefficient_spread * proof_length / expected
    
    return {
        "metric_name": "spread_times_proof_length",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - 1) < 0.1,  # Allow some tolerance
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / sum(1 for r in results if r["metric_value"] is not None)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / (sum(1 for r in results if r["metric_value"] is not None) - 1))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")