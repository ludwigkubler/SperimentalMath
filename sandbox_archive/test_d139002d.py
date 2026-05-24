# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        return [[random.choice([1, -1]) for _ in range(n)] for _ in range(2**n)]
    
    def resolution_width(cnf):
        n = len(cnf[0])
        clauses = cnf[:]
        width = 0
        while clauses:
            new_clauses = []
            for clause in clauses:
                if not any(abs(lit) == abs(clause[0]) for lit in clause):
                    new_clauses.append(clause)
                else:
                    for other_clause in clauses:
                        if set([abs(lit) for lit in clause]) & set([abs(lit) for lit in other_clause]):
                            new_lit = -clause[0] * other_clause[0]
                            new_clause = [lit for lit in clause + other_clause if abs(lit) != abs(new_lit)]
                            new_clauses.append(new_clause)
            clauses = new_clauses
            width += 1
        return width
    
    def noncommutative_crossed_product(n):
        G = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                G[i][j] = (-1)**(i & j)
        return G
    
    def minimal_rank(G):
        rank = 0
        for row in G:
            if any(row):
                rank += 1
        return rank
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    width = resolution_width(cnf)
    G = noncommutative_crossed_product(n)
    r_G_f = minimal_rank(G)
    
    if width == 0:
        return {
            "metric_name": "r(G_f) / w(CNF(f))",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Resolution proof width is zero"
        }
    
    ratio = Fraction(r_G_f, width)
    return {
        "metric_name": "r(G_f) / w(CNF(f))",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": True if ratio <= 2 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "unknown"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")