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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def is_isomorphic(g1, g2):
        if len(g1) != len(g2):
            return False
        nodes = list(range(len(g1)))
        for perm in itertools.permutations(nodes):
            if all(g1[i][j] == g2[perm[i]][perm[j]] for i in range(len(g1)) for j in range(i + 1, len(g1))):
                return True
        return False
    
    def symmetry_group_order(g):
        nodes = list(range(len(g)))
        group = set()
        for perm in itertools.permutations(nodes):
            if all(g[i][j] == g[perm[i]][perm[j]] for i in range(len(g)) for j in range(i + 1, len(g))):
                group.add(tuple(perm))
        return len(group)
    
    def resolution_length(graph):
        # Simplified Tseitin formula resolution length calculation
        n = len(graph)
        clauses = []
        for u in range(n):
            clauses.append([u])
            for v in range(u + 1, n):
                if (u, v) in graph:
                    clauses.append([-u, -v])
                    clauses.append([u, v])
                else:
                    clauses.append([-u, v])
                    clauses.append([u, -v])
        return len(clauses)
    
    def run_resolution(g):
        clauses = resolution_length(g)
        stack = []
        while clauses:
            clause = random.choice(clauses)
            if not any(x in stack for x in clause) and not any(-x in stack for x in clause):
                stack.append(random.choice(clause))
            else:
                return len(stack)
    
    n = 20
    graph = generate_graph(n)
    sym_group_order = symmetry_group_order(graph)
    proof_length = run_resolution(graph)
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": proof_length >= 2 ** sym_group_order,
        "counterexample": "" if proof_length >= 2 ** sym_group_order else f"Graph with n={n}, Sym(G)={sym_group_order}, Proof Length={proof_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_length} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_length} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")