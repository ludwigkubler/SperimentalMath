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
    
    def generate_instance(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(lit not in -clause for lit in clause):
                clauses.append(clause)
        return clauses
    
    def local_coherence(clauses):
        n = len(clauses[0])
        count = 0
        for i, clause in enumerate(clauses):
            for j in range(i + 1, len(clauses)):
                if any(lit in clause and -lit in clauses[j] for lit in set(clause) | set(clauses[j])):
                    count += 1
        return Fraction(count, n * (n - 1))
    
    def dpll_path_length(clauses):
        stack = []
        assignment = [None] * len(clauses[0])
        
        def dfs():
            if not stack:
                return 1
            literal = stack.pop()
            pos_lit, neg_lit = abs(literal), -literal
            if assignment[pos_lit - 1] == neg_lit or assignment[neg_lit - 1] == pos_lit:
                return 0
            if assignment[pos_lit - 1] is None:
                assignment[pos_lit - 1] = pos_lit
                stack.append(-pos_lit)
                path_length = dfs()
                if path_length > 0:
                    return path_length + 1
                assignment[pos_lit - 1] = None
            if assignment[neg_lit - 1] is None:
                assignment[neg_lit - 1] = neg_lit
                stack.append(pos_lit)
                path_length = dfs()
                if path_length > 0:
                    return path_length + 1
                assignment[neg_lit - 1] = None
            return 0
        
        for clause in clauses:
            stack.extend(clause)
        return dfs()
    
    n_max = 40
    instances_tested = 0
    total_coherence = 0
    total_path_length = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clauses = generate_instance(n)
            coherence = local_coherence(clauses)
            if coherence < Fraction(n**(2/3), 1):
                path_length = dpll_path_length(clauses)
                total_path_length += path_length
            else:
                total_path_length += n**(1/3)
            total_coherence += coherence
            instances_tested += 1
    
    mean_coherence = total_coherence / instances_tested
    mean_path_length = total_path_length / instances_tested
    
    conjecture_holds = all(coherence >= Fraction(n**(2/3), 1) for n in [5, 10, 15, 20, 30, 40] for _ in range(5))
    
    return {
        "metric_name": "local_coherence",
        "metric_value": mean_coherence,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_coherence = sum(r["metric_value"] for r in results) / len(results)
    std_coherence = math.sqrt(sum((r["metric_value"] - mean_coherence)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_coherence} std={std_coherence} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=mapping_undefined first_failing_seed=NA")
    else:
        print(f"RESULT: INCONCLUSIVE reason=support_fraction={support_fraction}")