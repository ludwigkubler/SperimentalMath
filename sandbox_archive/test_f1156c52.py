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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def algebraic_automorphism_group(cnf):
        n = len(cnf)
        generators = set()
        
        # Find a generator for the automorphism group
        for i in range(n):
            gen = {j + 1 if j < i else -j - 1 for j in range(n)}
            if all(all((lit in gen or -lit in gen) == (other_lit in gen or -other_lit in gen) for other_clause in cnf for other_lit in other_clause) for clause in cnf):
                generators.add(tuple(sorted(gen)))
        
        return len(generators)
    
    def circuit_satisfiability_complexity(cnf):
        n = len(cnf)
        stack = []
        assignment = [False] * (n + 1)
        
        def dpll():
            if not cnf:
                return True
            literal = next((lit for lit in range(1, n + 1) if all(lit not in clause and -lit not in clause for clause in cnf)), None)
            if literal is None:
                return False
            
            assignment[literal] = True
            stack.append(literal)
            new_cnf = [clause for clause in cnf if literal not in clause and -literal not in clause]
            if dpll():
                return True
            
            assignment[literal] = False
            stack.pop()
            assignment[-literal] = True
            new_cnf = [clause for clause in cnf if -literal not in clause and literal not in clause]
            if dpll():
                return True
            
            assignment[-literal] = False
            return False
        
        return 1 if dpll() else 0
    
    n_max = 40
    instances_tested = 0
    circuit_ranks = []
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            rank = algebraic_automorphism_group(cnf)
            complexity = circuit_satisfiability_complexity(cnf)
            
            if rank is not None and complexity is not None:
                circuit_ranks.append((rank, complexity))
                instances_tested += 1
    
    if not circuit_ranks:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ranks, complexities = zip(*circuit_ranks)
    correlation_coefficient = sum((r - mean_ranks) * (c - mean_complexities) for r, c in circuit_ranks) / instances_tested
    mean_ranks = sum(ranks) / instances_tested
    mean_complexities = sum(complexities) / instances_tested
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient <= 3 and len([c for c in circuit_ranks if c[1] > 0]) / instances_tested >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    metric_mean = sum(r["metric_value"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={metric_mean} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={metric_mean} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not enough data\" first_failing_seed={first_failing_seed}")