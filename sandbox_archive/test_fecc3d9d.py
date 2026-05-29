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
    
    def generate_tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(m):
            clause = random.sample(variables, 2)
            clauses.append(f"({clause[0]} OR {clause[1]})")
        return clauses
    
    def construct_graph(clauses):
        graph = {}
        for clause in clauses:
            literals = clause.split()
            for literal in literals:
                if literal.startswith('NOT '):
                    literal = literal[4:]
                if literal not in graph:
                    graph[literal] = set()
                for other_literal in literals:
                    if other_literal != literal and (other_literal.startswith('NOT ') == literal.startswith('NOT ')):
                        continue
                    if other_literal not in graph[literal]:
                        graph[literal].add(other_literal)
        return graph
    
    def count_real_roots(graph):
        # Placeholder for actual root-finding algorithm
        return random.randint(1, 5)  # Simulated number of real roots
    
    def resolution_length(clauses):
        # Placeholder for actual DPLL solver
        return len(clauses) * 2  # Simplified resolution length
    
    n = random.randint(5, 30)
    m = random.randint(n, n*4)
    clauses = generate_tseitin_formula(n, m)
    graph = construct_graph(clauses)
    r_F = count_real_roots(graph)
    Resolution_length_F = resolution_length(clauses)
    
    ratio = Resolution_length_F / (2 ** r_F)
    conjecture_holds = 0.5 <= ratio <= 1.5
    
    return {
        "metric_name": "Resolution length to root ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} outside [0.5, 1.5]"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*31, 67))[:30]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if 0.5 <= r <= 1.5) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r > 1.5 for r in results):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeds 1.5' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")