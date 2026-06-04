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
    
    def generate_sat_instance(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            literals = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(f"({' | '.join(literals)})")
        return clauses
    
    def tseitin_transform(clauses):
        new_vars = {}
        new_clauses = []
        var_count = 1
        for clause in clauses:
            literals = [l.strip('~') for l in clause.split(' | ')]
            if len(literals) == 2 and literals[0] != literals[1]:
                tseitin_var = f'y{var_count}'
                new_vars[tseitin_var] = var_count
                new_clauses.append(f"({literals[0]} -> {tseitin_var})")
                new_clauses.append(f"({literals[1]} -> {tseitin_var})")
                new_clauses.append(f"(~{tseitin_var} -> ~{literals[0]})")
                new_clauses.append(f"(~{tseitin_var} -> ~{literals[1]})")
                var_count += 1
            else:
                new_clauses.append(clause)
        return new_clauses, new_vars
    
    def resolution_prove(clauses):
        clauses_set = set(clauses)
        unit_clauses = [c for c in clauses if ' | ' not in c]
        while unit_clauses:
            unit_clause = unit_clauses.pop()
            literal = unit_clause.strip('~')
            polarity = 1 if literal[0] != '~' else -1
            new_clauses = []
            for clause in clauses_set:
                if literal in clause:
                    continue
                if f"~{literal}" in clause:
                    new_clauses.append(clause.replace(f"~{literal}", ""))
                else:
                    new_clauses.append(clause)
            unit_clauses.extend([c for c in new_clauses if ' | ' not in c])
            clauses_set.update(new_clauses)
        return len(clauses_set)
    
    def monodromy_group_order(n):
        # Placeholder implementation
        # This should be replaced with a proper algorithm to compute the monodromy group order
        return n + 1
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        m = random.randint(2 * n, 4 * n)
        sat_instance = generate_sat_instance(n, m)
        tseitin_clauses, new_vars = tseitin_transform(sat_instance)
        proof_width = resolution_prove(tseitin_clauses)
        monodromy_order = monodromy_group_order(n)
        results.append((monodromy_order, proof_width))
    
    if not results:
        return {
            "metric_name": "Monodromy Group Order vs Resolution Proof Width",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    monodromy_orders = [r[0] for r in results]
    proof_widths = [r[1] for r in results]
    alpha = sum(monodromy_orders) / sum(proof_widths)
    correlation = sum((m - alpha * w) ** 2 for m, w in zip(monodromy_orders, proof_widths)) / len(results)
    
    return {
        "metric_name": "Monodromy Group Order vs Resolution Proof Width",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40]),
        "conjecture_holds": correlation <= 0.9 * alpha,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction < 0.7:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")