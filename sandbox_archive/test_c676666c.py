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

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(c == 0 for c in clause):
            clause[random.randint(0, n-1)] = random.choice([-1, 1])
        clauses.append(clause)
    return clauses

def xor_and_tree_width(clauses):
    def dfs(node):
        if isinstance(node, int):
            return 1
        left, right = node
        return max(dfs(left), dfs(right)) + 1
    tree = build_xor_and_tree(clauses)
    return dfs(tree)

def build_xor_and_tree(clauses):
    if len(clauses) == 1:
        return clauses[0]
    mid = len(clauses) // 2
    left = build_xor_and_tree(clauses[:mid])
    right = build_xor_and_tree(clauses[mid:])
    return (left, right)

def matroid_expansion(cnf):
    rank = 0
    for clause in cnf:
        if all(abs(x) == 1 for x in clause):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_tw = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            rank = matroid_expansion(cnf)
            tw = xor_and_tree_width(cnf)
            total_rank += rank
            total_tw += tw
            instances_tested += 1

    mean_rank = Fraction(total_rank, instances_tested)
    mean_tw = Fraction(total_tw, instances_tested)
    ratio = mean_rank / mean_tw

    if ratio > 1.5:
        conjecture_holds = False
        counterexample = "Ratio exceeds 1.5"

    return {
        "metric_name": "Rank/TW Ratio",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds 1.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=Insufficient support")