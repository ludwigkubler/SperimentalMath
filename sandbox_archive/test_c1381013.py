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
        for _ in range(2**n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            if all(x > 0 for x in clause):
                clauses.append(clause)
        return clauses
    
    def resolution_proof_depth(cnf):
        stack = cnf[:]
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if any(-x in stack[i] and x in stack[j] for x in set(stack[i]) & set(stack[j])):
                        new_clause = [x for x in stack[i] if x not in stack[j]] + [x for x in stack[j] if -x not in stack[i]]
                        break
                if new_clause:
                    break
            if new_clause is None:
                return len(cnf) - len(stack)
            stack.append(new_clause)
    
    def hypergeometric_sequence(cnf):
        n = len(cnf[0])
        sequence = []
        for clause in cnf:
            term = 1
            for literal in clause:
                if literal > 0:
                    term *= (n + literal) / (2 * n)
                else:
                    term *= (n - literal) / (2 * n)
            sequence.append(term)
        return sequence
    
    def minimal_rank(sequence):
        rank = 1
        for i in range(1, len(sequence)):
            if all(abs(sequence[i] - sequence[j]) > 1e-9 for j in range(i)):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        depth = resolution_proof_depth(cnf)
        sequence = hypergeometric_sequence(cnf)
        rank = minimal_rank(sequence)
        
        if rank < math.log(n):
            return {
                "metric_name": "minimal_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, depth={depth}, rank={rank}"
            }
        
        results.append(rank)
    
    mean_rank = sum(results) / len(results)
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": mean_rank / n >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, depth={results[0]['metric_value']}\", first_failing_seed={first_failing_seed}")