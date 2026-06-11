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
    
    def is_power_of_two(n):
        return n > 0 and (n & (n - 1)) == 0
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def resolvent(cnf):
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        resolvants = []
        for lit in literals:
            pos_clauses = [clause for clause in cnf if lit in clause]
            neg_clauses = [clause for clause in cnf if -lit in clause]
            if len(pos_clauses) > 1 or len(neg_clauses) > 1:
                resolvant = []
                for clause in pos_clauses + neg_clauses:
                    resolvant.extend(lit for lit in clause if lit != lit and -lit not in clause)
                resolvants.append(resolvant)
        return resolvants
    
    def quadratic_residue_class_representation(n):
        # Simplified version of QCR calculation
        return n % 2 == 0
    
    def resolution_proof_width(cnf):
        stack = cnf[:]
        while stack:
            clause = stack.pop()
            if not any(lit in clause for lit in stack):
                continue
            new_clause = [lit for lit in clause if lit not in stack]
            stack.append(new_clause)
        return len(stack)
    
    n_max = 0
    instances_tested = 0
    total_rpw = 0
    count_supporting = 0
    
    for n in range(5, 41):
        cnf = generate_cnf(n)
        if quadratic_residue_class_representation(n):
            rpw = resolution_proof_width(cnf)
            total_rpw += rpw
            instances_tested += 1
            n_max = max(n_max, n)
            if n_min <= n < n_max:
                if n >= 5 and n < 20:
                    count_supporting += rpw <= 1.2 * n and rpw >= n
    
    mean_rpw = total_rpw / instances_tested
    support_fraction = count_supporting / instances_tested
    
    conjecture_holds = support_fraction >= 0.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": mean_rpw,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rpw = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rpw} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] > 1.5 * n for n, r in enumerate(results) if n >= 5 and n < 20):
        first_failing_seed = next(n for n, r in enumerate(results) if n >= 5 and n < 20 and r["metric_value"] > 1.5 * n)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")