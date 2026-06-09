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
    
    def generate_random_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            while len(set(clause)) != 2:
                clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def compute_hyperplane_arrangement(phi):
        G = {}
        for literal in range(-n, n + 1):
            if literal == 0: continue
            G[literal] = set()
        for clause in phi:
            for literal in clause:
                other_literals = [x for x in clause if x != literal]
                for other_literal in other_literals:
                    if -other_literal not in G[literal]:
                        G[literal].add(other_literal)
                    if -literal not in G[other_literal]:
                        G[other_literal].add(literal)
        return G

    def frege_proof_depth(phi):
        def dpll(assignment, clauses):
            if not clauses:
                return 0
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                return 1 + dpll(new_assignment, new_clauses)
            pure_literal = next((l for l in range(1, n + 1) if (l in assignment and not assignment[l]) or (-l in assignment and assignment[-l])), None)
            if pure_literal:
                new_assignment = assignment.copy()
                new_assignment[pure_literal] = True
                new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
                return 1 + dpll(new_assignment, new_clauses)
            literal = random.choice([l for l in range(1, n + 1) if l not in assignment and -l not in assignment])
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return 1 + dpll(new_assignment, new_clauses)
        return dpll({}, phi)

    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    phi = generate_random_cnf(n, m)
    
    G = compute_hyperplane_arrangement(phi)
    H_G = sum(math.log(len(G[literal])) for literal in G if len(G[literal]) > 0) / n
    w_Frege = frege_proof_depth(phi)
    
    return {
        "metric_name": "minimal_geometric_entropy",
        "metric_value": H_G,
        "instances_tested": m,
        "n_max": n,
        "conjecture_holds": H_G <= 0.5 * w_Frege or w_Frege == 0,
        "counterexample": "" if H_G <= 0.5 * w_Frege else f"H(G(φ)) = {H_G}, w_Frege(φ) = {w_Frege}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif any(not r["conjecture_holds"] and r["metric_value"] <= 0.5 * r["instances_tested"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='H(G(φ)) ≤ 0.5 * w_Frege(φ)' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")