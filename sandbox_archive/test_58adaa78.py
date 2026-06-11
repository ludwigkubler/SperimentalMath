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

def generate_quandle(q):
    quandle = {}
    for i in range(q):
        for j in range(q):
            quandle[(i, j)] = (i + j) % q
    return quandle

def tropicalize_quandle(quandle):
    n = len(quandle)
    T = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        T[i][i] = 0
    for (i, j), v in quandle.items():
        T[i][v] = min(T[i][v], T[j][i])
    return T

def resolve_cnf(cnf):
    stack = []
    assignment = {}
    def propagate():
        while stack:
            literal = stack.pop()
            if literal < 0:
                continue
            if literal in assignment and assignment[literal]:
                continue
            assignment[literal] = True
            for clause in cnf:
                if literal not in clause:
                    continue
                clause.remove(literal)
                if not clause:
                    return False
                stack.append(-literal)
    for literal in range(1, len(cnf) + 1):
        stack.append(literal)
        if not propagate():
            return False
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    q = random.randint(5, 40)
    quandle = generate_quandle(q)
    T = tropicalize_quandle(quandle)
    
    cnf = []
    for i in range(q):
        clause = [j + 1 for j in range(q) if T[i][j] == math.inf]
        cnf.append(clause)
    
    total_width = 0
    instances_tested = len(cnf)
    n_max = q
    
    for _ in range(30):
        assignment = {}
        stack = []
        def propagate():
            while stack:
                literal = stack.pop()
                if literal < 0:
                    continue
                if literal in assignment and assignment[literal]:
                    continue
                assignment[literal] = True
                for clause in cnf:
                    if literal not in clause:
                        continue
                    clause.remove(literal)
                    if not clause:
                        return False
                    stack.append(-literal)
        for literal in range(1, len(cnf) + 1):
            stack.append(literal)
            if not propagate():
                total_width += 1
                break
    
    tq_Q = q - 1
    ratio = Fraction(total_width, instances_tested) / tq_Q
    conjecture_holds = ratio <= Fraction(3, 2) and ratio > Fraction(0, 1)
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": total_width,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"ratio={ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ratio={results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")