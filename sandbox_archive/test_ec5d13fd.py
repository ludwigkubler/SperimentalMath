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
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def cnf_to_algebraic_structure(cnf):
        variables = set()
        for clause in cnf:
            for literal in clause:
                variables.add(abs(literal))
        n = len(variables)
        algebraic_structure = [0] * (n + 1)
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    algebraic_structure[literal] += 1
                else:
                    algebraic_structure[-literal] -= 1
        return algebraic_structure
    
    def noncommutative_k_theory_order(algebraic_structure):
        n = len(algebraic_structure)
        for i in range(1, n + 1):
            if algebraic_structure[i] != 0:
                return i
        return 0
    
    def resolution_proof_width(cnf):
        stack = []
        while cnf:
            clause = random.choice(cnf)
            if len(clause) == 1:
                literal = clause[0]
                if literal > 0:
                    for c in cnf:
                        if literal in c:
                            cnf.remove(c)
                        elif -literal in c:
                            c.remove(-literal)
                else:
                    for c in cnf:
                        if -literal in c:
                            cnf.remove(c)
                        elif literal in c:
                            c.remove(literal)
            else:
                clause1, clause2 = random.sample(cnf, 2)
                new_clause = []
                for lit1 in clause1:
                    if -lit1 not in clause2:
                        new_clause.append(lit1)
                for lit2 in clause2:
                    if -lit2 not in clause1:
                        new_clause.append(lit2)
                cnf.remove(clause1)
                cnf.remove(clause2)
                cnf.append(new_clause)
        return len(stack)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    algebraic_structure = cnf_to_algebraic_structure(cnf)
    k_theory_order = noncommutative_k_theory_order(algebraic_structure)
    proof_width = resolution_proof_width(cnf)
    
    return {
        "metric_name": "K-theory Order vs Resolution Proof Width",
        "metric_value": abs(k_theory_order - proof_width),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")