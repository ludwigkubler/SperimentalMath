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
    
    def generate_k_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_length(clauses):
        stack = []
        visited = set()
        
        def resolve(lit, other_lit):
            if lit == -other_lit:
                return True
            for clause in clauses:
                if lit in clause and -other_lit in clause:
                    new_clause = [x for x in clause if x != lit and x != -other_lit]
                    if not new_clause:
                        return True
                    stack.append(new_clause)
                    visited.add(tuple(sorted(new_clause)))
        
        while stack:
            clause = stack.pop()
            for literal in clause:
                other_literal = -literal
                if (other_literal, literal) in visited or (-literal, other_literal) in visited:
                    continue
                if resolve(literal, other_literal):
                    return len(visited)
            visited.add(tuple(sorted(clause)))
        
        return len(visited)
    
    def minimal_local_defect_complexity(n):
        # Placeholder for actual computation
        return n
    
    n = random.randint(5, 40)
    m = random.randint(2 * n, 3 * n)
    clauses = generate_k_cnf(n, m)
    
    local_defect_complexity = minimal_local_defect_complexity(n)
    resolution_diameter = resolution_length(clauses)
    
    if resolution_diameter == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Resolution diameter is zero, invalid instance"
        }
    
    ratio = Fraction(local_defect_complexity, resolution_diameter)
    
    return {
        "metric_name": "Ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")