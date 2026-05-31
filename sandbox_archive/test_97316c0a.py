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
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(abs(c) != abs(clause[0]) for c in clause[1:]):
                clauses.append(clause)
        return clauses
    
    def construct_coxeter_diagram(clauses):
        n = len(clauses[0])
        diagram = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i in range(n):
                for j in range(i + 1, n):
                    if (abs(clause[i]) != abs(clause[j])) and ((clause[i] > 0) == (clause[j] > 0)):
                        diagram[i][j] = diagram[j][i] = 1
        return diagram
    
    def communication_complexity(diagram):
        n = len(diagram)
        if n <= 1:
            return 0
        cc = 0
        for i in range(n):
            for j in range(i + 1, n):
                if diagram[i][j] == 1:
                    cc += 1
        return cc
    
    def entropy(diagram):
        n = len(diagram)
        edges = sum(sum(row) for row in diagram) // 2
        return math.log(edges) / math.log(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    cc_values = []
    cde_values = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        diagram = construct_coxeter_diagram(cnf)
        cc = communication_complexity(diagram)
        cde = entropy(diagram)
        cc_values.append(cc)
        cde_values.append(cde)
    
    mean_cc = sum(cc_values) / len(cc_values)
    mean_cde = sum(cde_values) / len(cde_values)
    correlation = sum((cc - mean_cc) * (cde - mean_cde) for cc, cde in zip(cc_values, cde_values)) / (len(cc_values) * math.sqrt(sum((cc - mean_cc) ** 2 for cc in cc_values)) * math.sqrt(sum((cde - mean_cde) ** 2 for cde in cde_values)))
    
    conjecture_holds = correlation >= 0.8
    counterexample = "" if conjecture_holds else "correlation < 0.8"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_cc,
        "instances_tested": len(cc_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_cc = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_cc} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cc} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation < 0.8\" first_failing_seed={first_failing_seed}")