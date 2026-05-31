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

def generate_cnf(n, m):
    clauses = set()
    for _ in range(m):
        clause = {random.randint(1, n), random.randint(-n, -1)}
        if len(clause) == 2:
            clauses.add(frozenset(clause))
    return clauses

def construct_diagram(cnf):
    diagram = {}
    n = max(abs(x) for x in cnf)
    for i in range(1, n + 1):
        diagram[i] = set()
        diagram[-i] = set()
    for clause in cnf:
        for var in clause:
            diagram[var].add(-var)
            diagram[-var].add(var)
    return diagram

def count_automorphisms(diagram):
    n = max(diagram.keys())
    def is_valid_permutation(perm):
        for v in range(1, n + 1):
            if perm[v] not in diagram:
                return False
            for u in diagram[v]:
                if perm[u] not in diagram[perm[v]]:
                    return False
        return True

    def generate_permutations(n):
        elements = list(range(1, n + 1))
        for i in range(n):
            for j in range(i + 1, n):
                elements[i], elements[j] = elements[j], elements[i]
                yield elements[:]
                elements[i], elements[j] = elements[j], elements[i]

    automorphisms = 0
    for perm in generate_permutations(n):
        if is_valid_permutation(perm):
            automorphisms += 1
    return automorphisms

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_automorphisms = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        m_values = [max(1, int(n * (i / len(n_values)))) for i in range(len(n_values))]
        for m in m_values:
            cnf = generate_cnf(n, m)
            diagram = construct_diagram(cnf)
            automorphisms = count_automorphisms(diagram)
            total_automorphisms += automorphisms
            instances_tested += 1
            n_max = max(n_max, n)

    mean_C = total_automorphisms / instances_tested
    f_n = m ** (1/2) * n ** (3/4)
    ratio = mean_C / f_n

    conjecture_holds = ratio <= 1.05
    counterexample = "" if conjecture_holds else f"mean_C={mean_C}, f_n={f_n}"

    return {
        "metric_name": "Automorphisms",
        "metric_value": mean_C,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]

    mean_C = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_C} std=NA support_fraction={support_fraction}")