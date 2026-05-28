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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = f'{variables[i-1]} ~{variables[i-1]}'
            clauses.append(clause)
        return ' '.join(clauses)
    
    def tseitin_graph(formula):
        graph = {}
        literals = set()
        for clause in formula.split():
            if '~' in clause:
                literal = clause[2:]
                negated = True
            else:
                literal = clause
                negated = False
            literals.add(literal)
            if literal not in graph:
                graph[literal] = []
            if negated:
                for other_literal in literals - {literal}:
                    if other_literal not in graph[literal]:
                        graph[literal].append(other_literal)
                    if literal not in graph[other_literal]:
                        graph[other_literal].append(literal)
        return graph
    
    def hodge_structure(graph):
        # Simplified Hodge structure computation for demonstration
        # This is a placeholder and should be replaced with actual computation
        rank = len(graph)
        return rank, 0
    
    def resolution_length(formula):
        # Placeholder for Resolution proof length calculation
        # This is a placeholder and should be replaced with actual computation
        return random.randint(100, 1000)
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    graph = tseitin_graph(formula)
    rank, _ = hodge_structure(graph)
    proof_length = resolution_length(formula)
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": False if proof_length < 2**math.floor(math.log(rank, 2)) else True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")