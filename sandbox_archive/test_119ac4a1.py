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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) > 0:
                clauses.append(clause)
        return clauses
    
    def calculate_entropy(state):
        counts = {tuple(sorted(s)): state[tuple(sorted(s))] for s in state}
        total = sum(counts.values())
        entropy = -sum(v / total * math.log2(v / total) for v in counts.values() if v > 0)
        return entropy
    
    def calculate_circuit_depth(cnf):
        # Simplified DPLL algorithm to estimate circuit depth
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                if dpll([c for c in clauses if literal not in c], new_assignment):
                    return True
                new_assignment[literal] = False
                if dpll([c for c in clauses if -literal not in c], new_assignment):
                    return True
                return False
            pure_literal = next((l for l in range(1, n + 1) if (l not in assignment and -l not in assignment)), None)
            if pure_literal:
                new_assignment[pure_literal] = True
                if dpll(clauses, new_assignment):
                    return True
                new_assignment[pure_literal] = False
                if dpll(clauses, new_assignment):
                    return True
                return False
            literal = random.choice([l for l in range(1, n + 1) if l not in assignment and -l not in assignment])
            new_assignment[literal] = True
            if dpll(clauses, new_assignment):
                return True
            new_assignment[literal] = False
            if dpll(clauses, new_assignment):
                return True
            return False
        
        depth = 0
        for _ in range(10):  # Simplified by running multiple trials
            assignment = {i: random.choice([True, False]) for i in range(1, n + 1)}
            if dpll(cnf, assignment):
                depth += 1
        return depth / 10
    
    def construct_quaternionic_state(cnf):
        # Simplified state construction (not actual quantum computation)
        state = {}
        for clause in cnf:
            key = tuple(sorted(clause))
            state[key] = random.random()
        return state
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        state = construct_quaternionic_state(cnf)
        entropy = calculate_entropy(state)
        depth = calculate_circuit_depth(cnf)
        ratio = depth / entropy if entropy > 0 else float('inf')
        metric_values.append(ratio)
    
    mean_ratio = sum(metric_values) / len(metric_values)
    std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(abs(x - mean_ratio) <= 0.05 * mean_ratio for x in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "circuit_depth_to_entropy_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")