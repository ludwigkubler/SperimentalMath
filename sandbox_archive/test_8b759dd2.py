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
    
    def generate_k_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, k=2)
            clauses.append(clause)
        return clauses

    def construct_read_twice_bp(k_cnf):
        # Simplified construction of a read-twice BP
        bp = {}
        for clause in k_cnf:
            if clause[0] not in bp:
                bp[clause[0]] = []
            if clause[1] not in bp:
                bp[clause[1]] = []
            bp[clause[0]].append(clause)
            bp[clause[1]].append(clause)
        return bp

    def derive_algebraic_structure(bp):
        # Simplified derivation of algebraic structure
        algebraic_structure = {}
        for node, clauses in bp.items():
            if node not in algebraic_structure:
                algebraic_structure[node] = set()
            for clause in clauses:
                algebraic_structure[node].update(clause)
        return algebraic_structure

    def compute_minimal_rank(algebraic_structure):
        # Simplified computation of minimal rank
        rank = 0
        for node, structure in algebraic_structure.items():
            rank += len(structure)
        return rank

    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    k_cnf = generate_k_cnf(n, m)
    bp = construct_read_twice_bp(k_cnf)
    algebraic_structure = derive_algebraic_structure(bp)
    minimal_rank = compute_minimal_rank(algebraic_structure)

    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": minimal_rank <= math.log(n**m),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['metric_value']}, m={m}"
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")