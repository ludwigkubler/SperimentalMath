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
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses

    def polynomial_from_clause(clause):
        x = Fraction(1)
        for literal in clause:
            x *= (Fraction(literal) + Fraction(abs(literal)))
        return x

    def resultant(poly1, poly2):
        if not poly1 or not poly2:
            return 0
        n = len(poly1)
        m = len(poly2)
        result = 0
        for i in range(n):
            for j in range(m):
                if poly1[i] != 0 and poly2[j] != 0:
                    result += poly1[i] * poly2[j]
        return result

    def degree_of_polynomial(poly):
        max_degree = 0
        for term in poly:
            degree = sum(abs(lit) for lit in term)
            if degree > max_degree:
                max_degree = degree
        return max_degree

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    polynomials = [polynomial_from_clause(clause) for clause in cnf]
    
    resultant_poly = polynomials[0]
    for poly in polynomials[1:]:
        resultant_poly = resultant(resultant_poly, poly)
    
    degree = degree_of_polynomial([resultant_poly])
    
    metric_value = 2 ** (n / math.log(2))
    conjecture_holds = degree >= metric_value
    counterexample = "" if conjecture_holds else f"Resultant degree {degree} < 2^{n/2}"
    
    return {
        "metric_name": "resultant_degree",
        "metric_value": degree,
        "instances_tested": n,
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
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")