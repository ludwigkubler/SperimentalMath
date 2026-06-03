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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(lit) != abs(clause[0]) for lit in clause[1:]):
                clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment):
        unsatisfied = [c for c in cnf if not any(lit in assignment and assignment[lit] == 1 for lit in c)]
        if not unsatisfied:
            return True
        unit_clause = next((c for c in unsatisfied if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0:
                assignment[-literal] = -1
            else:
                assignment[literal] = 1
            return dpll(cnf, assignment)
        pure_literal = next((lit for lit in range(1, len(assignment) + 1) if (lit not in assignment and -lit not in assignment)), None)
        if pure_literal is not None:
            assignment[pure_literal] = 1
            return dpll(cnf, assignment)
        literal = random.choice([l for l in range(1, len(assignment) + 1) if l not in assignment])
        assignment[literal] = 1
        if dpll(cnf, assignment):
            return True
        assignment[literal] = -1
        if dpll(cnf, assignment):
            return True
        return False
    
    def resolution_width(cnf):
        clauses = cnf[:]
        width = 0
        while True:
            unit_clauses = [c for c in clauses if len(c) == 1]
            if not unit_clauses:
                break
            unit_clause = unit_clauses[0]
            literal = unit_clause[0]
            new_clauses = []
            for c in clauses:
                if literal in c:
                    continue
                if -literal in c:
                    new_clauses.append([l for l in c if l != -literal])
                else:
                    new_clauses.append(c)
            clauses = new_clauses
            width += 1
        return width
    
    def max_reflections(n):
        vertices = list(range(1, n + 1))
        reflections = []
        while len(vertices) > 1:
            pivot = random.choice(vertices)
            reflection = [v for v in vertices if v != pivot]
            reflections.append(reflection)
            vertices = reflection
        return len(reflections)
    
    def pearson_correlation(xs, ys):
        n = len(xs)
        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        cov_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / n
        var_x = sum((x - mean_x)**2 for x in xs) / n
        var_y = sum((y - mean_y)**2 for y in ys) / n
        return cov_xy / math.sqrt(var_x * var_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    resolution_widths = []
    max_reflections_counts = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        width = resolution_width(cnf)
        resolution_widths.append(width)
        reflections_count = max_reflections(n)
        max_reflections_counts.append(reflections_count)
    
    correlation = pearson_correlation(resolution_widths, max_reflections_counts)
    p_value = 1.0  # Placeholder for actual p-value calculation
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.5 and p_value <= 0.05,
        "counterexample": "" if abs(correlation) >= 0.5 and p_value <= 0.05 else "correlation too weak or p-value too high"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation too weak or p-value too high\" first_failing_seed={first_failing_seed}")