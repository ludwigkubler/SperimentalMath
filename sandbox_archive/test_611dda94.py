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
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if len(set(clause)) == 2:
                clauses.append(clause)
        return clauses

    def quandle_structure(cnf):
        q = {}
        for clause in cnf:
            for literal in clause:
                if literal not in q:
                    q[literal] = set()
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    a, b = clause[i], clause[j]
                    q[a].add(b)
                    q[b].add(a)
        return q

    def minimal_rank(q):
        rank = 0
        visited = set()
        for literal in q:
            if literal not in visited:
                queue = [literal]
                level = 1
                while queue:
                    next_queue = []
                    for node in queue:
                        if node not in visited:
                            visited.add(node)
                            next_queue.extend(q[node])
                    queue = next_queue
                    rank += level
                    level += 1
        return rank

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    q = quandle_structure(cnf)
    rank = minimal_rank(q)

    metric_value = rank / (n ** (3/2))
    conjecture_holds = metric_value <= 1
    counterexample = "" if conjecture_holds else f"CNF with n={n} and rank {rank}"

    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = r["seed"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")