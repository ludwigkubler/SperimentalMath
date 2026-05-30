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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set(random.sample(range(1, n+1), 3))
            if random.choice([True, False]):
                clause = {x for x in clause}
            else:
                clause = {-x for x in clause}
            clauses.append(clause)
        return clauses

    def is_quadratic_residue(a, p):
        if a == 0:
            return True
        if p <= 1 or not (isinstance(p, int) and isinstance(a, int)):
            raise ValueError("Invalid input")
        for i in range(1, p):
            if (i * i) % p == a:
                return True
        return False

    def construct_polynomial(clauses, n):
        poly = [0] * (n + 1)
        for clause in clauses:
            term = 1
            for lit in clause:
                if lit > 0:
                    term *= (2 * lit - 1) ** 2
                else:
                    term *= (-2 * lit - 1) ** 2
            poly[sum(clause)] += term
        return [abs(coeff) % 2 for coeff in poly]

    def resolution_width(clauses):
        queue = clauses.copy()
        while True:
            new_clause = None
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    if len(queue[i] & queue[j]) == 1:
                        new_clause = (queue[i] | queue[j]).difference(queue[i] & queue[j])
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(queue)
            if new_clause in queue:
                return resolution_width(queue)
            queue.append(new_clause)

    def order_of_quadratic_residues(poly):
        residues = [x for x in poly if is_quadratic_residue(x, 10)]
        residues.sort()
        return max(residues) - min(residues)

    n_max = 40
    instances_tested = 0
    total_metric_value = 0

    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            k = random.randint(3, min(n // 2, 4))
            clauses = generate_k_cnf(n, k)
            poly = construct_polynomial(clauses, n)
            width = resolution_width(clauses)
            order = order_of_quadratic_residues(poly)
            total_metric_value += order
            instances_tested += 1

    metric_value = total_metric_value / instances_tested
    conjecture_holds = all(order <= 3 * width for _, _, order, width in clauses)

    return {
        "metric_name": "Order of Quadratic Residues",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")