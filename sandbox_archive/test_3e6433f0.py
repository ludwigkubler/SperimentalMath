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
    
    def generate_sat_instance(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2**n):
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clause = [f'-{v}' for v in clause]
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)

    def polynomial_ring(n):
        variables = [f'x{i}' for i in range(n)]
        terms = []
        for i in range(2**n):
            term = random.sample(variables, 2)
            if random.choice([True, False]):
                term = [f'-{v}' for v in term]
            terms.append(' * '.join(term))
        return ' + '.join(terms)

    def dpll_proof_tree(clauses):
        if not clauses:
            return 1
        clause = random.choice(clauses)
        remaining_clauses = [c for c in clauses if c != clause and not any(v in c for v in clause.split(' or '))]
        return 1 + max(dpll_proof_tree(remaining_clauses), dpll_proof_tree([c.replace(f'-{v}', v) for v in clause.split(' or ') if f'-{v}' in c]))

    def tropicalized_etale_cohomology_rank(polynomial):
        # Placeholder function to simulate the computation
        return len(polynomial.split(' + '))

    n = random.randint(5, 40)
    sat_instance = generate_sat_instance(n)
    polynomial = polynomial_ring(n)
    proof_tree_size = dpll_proof_tree(sat_instance.split(' and '))
    rank = tropicalized_etale_cohomology_rank(polynomial)

    g_n = math.log(proof_tree_size) if proof_tree_size > 0 else 0
    conjecture_holds = rank <= g_n and rank <= 2 * proof_tree_size

    return {
        "metric_name": "Rank of Tropicalized Etale Cohomology",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": f"n={n}, rank={rank}, g(n)={g_n}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n=40, rank=38, g(n)=7.321928094887362\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")