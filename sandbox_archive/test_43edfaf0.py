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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:  # Ensure the clause is not trivial
                clauses.append(clause)
        return clauses
    
    def polynomial_representation(clauses):
        poly = {}
        for clause in clauses:
            monomial = 1
            for var in clause:
                if var > 0:
                    monomial *= (var + 1) / 2
                else:
                    monomial *= (-var + 1) / 2
            poly[tuple(sorted(clause))] = monomial
        return poly
    
    def symmetric_group_action(poly, n):
        actions = {}
        for i in range(n):
            action = [i]
            for j in range(1, n):
                action.append((action[-1] + 1) % n)
            actions[tuple(action)] = poly
        return actions
    
    def count_orbits(poly, actions):
        orbits = set()
        for action in actions.values():
            orbit = frozenset(action.keys())
            if orbit not in orbits:
                orbits.add(orbit)
        return len(orbits)
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    poly = polynomial_representation(clauses)
    actions = symmetric_group_action(poly, n)
    orbit_count = count_orbits(poly, actions)
    
    if "read_once" in seed:
        expected_orbit_count = math.log(len(clauses))
    else:
        expected_orbit_count = n / 2
    
    return {
        "metric_name": "orbit_count",
        "metric_value": orbit_count,
        "instances_tested": 1,
        "conjecture_holds": orbit_count >= expected_orbit_count,
        "counterexample": "" if orbit_count >= expected_orbit_count else f"read_once={seed}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample={result['counterexample']} first_failing_seed={first_failing_seed}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")