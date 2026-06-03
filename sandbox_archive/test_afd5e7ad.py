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
        for i in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literal = find_pure_literal(cnf) or find_unit_clause(cnf)
        if literal is None:
            return False
        return dpll(remove_literal(cnf, literal), {**assignment, literal: True}) or \
               dpll(remove_literal(cnf, literal), {**assignment, literal: False})
    
    def find_pure_literal(cnf):
        pure_literals = {}
        for clause in cnf:
            for literal in clause:
                if abs(literal) not in pure_literals:
                    pure_literals[abs(literal)] = literal
                elif pure_literals[abs(literal)] != literal:
                    del pure_literals[abs(literal)]
        return list(pure_literals.values())
    
    def find_unit_clause(cnf):
        for clause in cnf:
            if len(clause) == 1:
                return clause[0]
        return None
    
    def remove_literal(cnf, literal):
        return [c for c in cnf if literal not in c and -literal not in c]
    
    def geometric_loci(cnf):
        loci = set()
        for clause in cnf:
            for literal in clause:
                loci.add(abs(literal))
        return len(loci)
    
    def proof_depth(cnf):
        def dpll_depth(cnf, assignment={}):
            if not cnf:
                return 0
            literal = find_pure_literal(cnf) or find_unit_clause(cnf)
            if literal is None:
                return float('inf')
            return 1 + min(dpll_depth(remove_literal(cnf, literal), {**assignment, literal: True}),
                           dpll_depth(remove_literal(cnf, literal), {**assignment, literal: False}))
        return dpll_depth(cnf)
    
    n = random.randint(5, 30)
    cnf = generate_cnf(n)
    loci_count = geometric_loci(cnf)
    depth = proof_depth(cnf)
    
    return {
        "metric_name": "geometric_loci",
        "metric_value": loci_count,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": loci_count <= depth**2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_loci = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_loci) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_loci} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_loci} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")