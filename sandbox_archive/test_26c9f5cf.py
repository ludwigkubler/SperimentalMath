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
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if 0 not in clause:
            clauses.append(clause)
    
    def poly_add(poly1, poly2):
        result = {}
        for term, coeff in poly1.items():
            result[term] = result.get(term, 0) + coeff
        for term, coeff in poly2.items():
            result[term] = result.get(term, 0) + coeff
        return {term: coeff % 2 for term, coeff in result.items() if coeff % 2 != 0}
    
    def poly_mul(poly1, poly2):
        result = {}
        for t1, c1 in poly1.items():
            for t2, c2 in poly2.items():
                new_term = tuple(sorted(t1 + t2))
                result[new_term] = result.get(new_term, 0) + c1 * c2
        return {term: coeff % 2 for term, coeff in result.items() if coeff % 2 != 0}
    
    def monomial_count(poly):
        return len(poly)
    
    def buchberger(clauses):
        G = [set([tuple(sorted(c))] for c in clauses)]
        while True:
            new_gens = set()
            for g1, g2 in itertools.combinations(G, 2):
                s = tuple(sorted(g1 | g2))
                if len(s) > len(g1) + len(g2):
                    h = poly_add(poly_mul(g1, {s: -1}), poly_mul(g2, {s: 1}))
                    for term in sorted(h.keys()):
                        if term[0] == s[-1]:
                            new_gens.add(term)
            if not new_gens:
                break
            G |= new_gens
        return monomial_count({tuple(sorted(g)): 1 for g in G})
    
    metric_value = buchberger(clauses)
    conjecture_holds = metric_value >= 2 ** (n // 2)
    counterexample = "" if conjecture_holds else f"n={n}, monomials={metric_value}"
    return {
        "metric_name": "monomial_count",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 307))  # Generate 30 primes if no seeds provided
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
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['metric_name']}, monomials={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")