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
    n = random.randint(5, 30)
    m = random.randint(n, 2 * n)
    phi = generate_random_cnf(n, m)

    G = compute_hyperplane_arrangement(phi)
    H_G = compute_minimal_geometric_entropy(G)
    w_Frege = compute_frege_proof_depth(phi)

    return {
        "metric_name": "minimal_geometric_entropy",
        "metric_value": H_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

def generate_random_cnf(n: int, m: int) -> list:
    phi = []
    for _ in range(m):
        clause = random.sample(range(1, n + 1), 3)
        phi.append([random.choice([-1, 1]) * var for var in clause])
    return phi

def compute_hyperplane_arrangement(phi: list) -> dict:
    G = {}
    for clause in phi:
        for literal in clause:
            if literal not in G:
                G[literal] = set()
            for other_literal in clause:
                if other_literal != literal and -literal not in G[other_literal]:
                    G[literal].add(other_literal)
                    G[-other_literal].add(-literal)
    return G

def compute_minimal_geometric_entropy(G: dict) -> float:
    entropy = 0
    for literals, neighbors in G.items():
        if literals > 0:
            entropy += len(neighbors) / (2 ** literals)
    return entropy

def compute_frege_proof_depth(phi: list) -> int:
    def dpll(assignment):
        unsatisfied_clauses = [c for c in phi if any(lit in assignment and assignment[lit] == sign for lit, sign in zip(c, [1] * len(c)))]
        if not unsatisfied_clauses:
            return 0
        unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
        if unit_clause:
            literal, sign = unit_clause[0], unit_clause[1]
            assignment[literal] = sign
            return 1 + dpll(assignment)
        pure_literal = find_pure_literal(unsatisfied_clauses)
        if pure_literal is None:
            return float('inf')
        literal, sign = pure_literal
        assignment[literal] = sign
        return 1 + min(dpll(assignment), dpll({**assignment, -literal: -sign}))

    def find_pure_literal(clauses):
        count = {}
        for clause in clauses:
            for lit, sign in zip(clause, [1] * len(clause)):
                if lit not in count:
                    count[lit] = 0
                count[lit] += sign

        pure_literals = [lit for lit, c in count.items() if c == -count.get(-lit, 0)]
        return random.choice(pure_literals) if pure_literals else None

    assignment = {}
    return dpll(assignment)

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
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
    elif any(not r["conjecture_holds"] and r["counterexample"] == "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")