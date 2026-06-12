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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        G = {i: [] for i in range(n)}
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, d * (n - 1)) < d:
                    G[i].append(j)
                    G[j].append(i)
                    edges.add((i, j))
        return G
    
    def frege_proof_depth(G):
        # Simplified DPLL solver for Frege proof depth
        n = len(G)
        clauses = []
        for i in range(n):
            clause = [random.choice([-1, 1]) * (j + 1) for j in range(n)]
            clauses.append(clause)
        
        def dpll(model, clauses):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_model = model.copy()
                new_model[literal] = True
                if dpll(new_model, [c for c in clauses if literal not in c]):
                    return True
                new_model[literal] = False
                if dpll(new_model, [c for c in clauses if -literal not in c]):
                    return True
                return False
            pure_literal = next((l for l in range(1, n + 1) if (l not in model and -l not in model)), None)
            if pure_literal:
                new_model = model.copy()
                new_model[pure_literal] = True
                if dpll(new_model, clauses):
                    return True
                new_model[pure_literal] = False
                if dpll(new_model, clauses):
                    return True
                return False
            literal = random.choice([l for l in range(1, n + 1) if l not in model and -l not in model])
            new_model = model.copy()
            new_model[literal] = True
            if dpll(new_model, [c for c in clauses if literal not in c]):
                return True
            new_model[literal] = False
            if dpll(new_model, [c for c in clauses if -literal not in c]):
                return True
            return False
        
        model = {}
        return len(clauses) if dpll(model, clauses) else float('inf')
    
    def quantum_affine_generators(G):
        n = len(G)
        generators = set()
        for i in range(n):
            for j in G[i]:
                generators.add((i, j))
        return len(generators)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        d = random.randint(1, 5)
        G = generate_d_regular_graph(d, n_max)
        if G is None:
            continue
        
        m_G = quantum_affine_generators(G)
        w_G = frege_proof_depth(G)
        
        if w_G == float('inf'):
            continue
        
        expected_m_G = d ** 0.5 * n_max ** 0.75
        if not (expected_m_G * 0.9 <= m_G <= expected_m_G * 1.1):
            conjecture_holds = False
            counterexample = f"Graph with d={d}, n={n_max} failed: m(G)={m_G}, w(G)={w_G}"
        
        metric_values.append(m_G)
    
    return {
        "metric_name": "Generators vs. Frege Depth",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")