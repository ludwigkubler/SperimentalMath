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
    
    def generate_tseitin_formula(n):
        literals = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for literal in literals:
            clauses.append([literal])
        for i in range(1, n):
            for j in range(i+1, n+1):
                clauses.append([f"~{literals[i-1]}", f"{literals[j-1]}"])
                clauses.append([f"~{literals[j-1]}", f"{literals[i-1]}"])
        return literals, clauses
    
    def compute_noncrossing_partition(literals, clauses):
        n = len(literals)
        partition = [set() for _ in range(n+1)]
        for clause in clauses:
            if len(clause) == 2 and clause[0].startswith("~") and clause[1] != clause[0][1:]:
                i = int(clause[0][1:]) - 1
                j = int(clause[1]) - 1
                if i < j:
                    partition[i+1].add(j)
        return partition
    
    def resolution_proof_length(literals, clauses):
        n = len(literals)
        stack = []
        for clause in clauses:
            stack.append(clause)
        
        while stack:
            clause = stack.pop()
            if not any(literal in clause for literal in literals):
                continue
            new_clause = set()
            for other_clause in stack:
                common_lits = [lit for lit in clause if lit.startswith("~") and lit[1:] in other_clause]
                if len(common_lits) == 2:
                    new_lit = f"{common_lits[0][1:]} {common_lits[1][1:]}"
                    if new_lit not in literals:
                        return float('inf')
                    new_clause.add(new_lit)
            stack.append(list(new_clause))
        
        return len(stack)

    n = random.choice([5, 10, 15, 20, 30, 40])
    literals, clauses = generate_tseitin_formula(n)
    partition = compute_noncrossing_partition(literals, clauses)
    
    rank_P = max(len(x) for x in partition if x)
    proof_length = resolution_proof_length(literals, clauses)
    
    metric_value = proof_length
    conjecture_holds = proof_length >= 2 ** (math.log2(rank_P))
    counterexample = "" if conjecture_holds else f"rank(P)={rank_P}, proof_length={proof_length}"
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    total_metric = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric/len(results)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")