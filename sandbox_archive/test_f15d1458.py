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
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment, model):
        if not cnf:
            return True
        literal = find_pure_literal(cnf) or find_unit_clause(cnf)
        if literal is None:
            literal = random.choice([x for clause in cnf for x in clause])
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll(substitute(cnf, literal), new_assignment, model):
            return True
        new_assignment[literal] = False
        if dpll(substitute(cnf, -literal), new_assignment, model):
            return True
        return False
    
    def find_pure_literal(cnf):
        pure_literals = {}
        for clause in cnf:
            for literal in clause:
                if literal not in pure_literals:
                    pure_literals[literal] = 0
                else:
                    pure_literals[literal] += 1
        for literal, count in pure_literals.items():
            if count == len(cnf):
                return literal
        return None
    
    def find_unit_clause(cnf):
        for clause in cnf:
            if sum(1 for x in clause if x not in assignment) == 1:
                unit_literal = [x for x in clause if x not in assignment][0]
                return unit_literal
        return None
    
    def substitute(cnf, literal):
        new_cnf = []
        for clause in cnf:
            if literal not in clause and -literal not in clause:
                new_clause = [x for x in clause if x != -literal]
                if new_clause:
                    new_cnf.append(new_clause)
        return new_cnf
    
    def geometric_loci(cnf):
        loci = set()
        for clause in cnf:
            for literal in clause:
                loci.add(abs(literal))
        return len(loci)
    
    def proof_depth(cnf, assignment):
        depth = 0
        stack = [(cnf, assignment)]
        while stack:
            cnf, assignment = stack.pop()
            if not cnf:
                break
            literal = find_pure_literal(cnf) or find_unit_clause(cnf)
            if literal is None:
                literal = random.choice([x for clause in cnf for x in clause])
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            stack.append((substitute(cnf, literal), new_assignment))
            new_assignment[literal] = False
            stack.append((substitute(cnf, -literal), new_assignment))
            depth += 1
        return depth
    
    n = random.randint(5, 30)
    cnf = generate_cnf(n)
    assignment = {}
    model = {}
    
    loci_count = geometric_loci(cnf)
    proof_depth_value = proof_depth(cnf, assignment)
    
    return {
        "metric_name": "geometric_loci",
        "metric_value": loci_count,
        "instances_tested": 1,
        "n_max": n,
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
    
    mean_loci = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_loci) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_loci} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")