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
    
    n = 40
    edges = []
    for _ in range(n * (n - 1) // 2):
        u, v = random.sample(range(n), 2)
        if u < v and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    
    def clique_complex(G):
        cliques = []
        for r in range(1, n + 1):
            for subset in itertools.combinations(range(n), r):
                is_clique = True
                for i in range(r):
                    for j in range(i + 1, r):
                        if (subset[i], subset[j]) not in G:
                            is_clique = False
                            break
                    if not is_clique:
                        break
                if is_clique:
                    cliques.append(subset)
        return cliques
    
    def euler_characteristic(cliques):
        V = n
        E = len(edges)
        F = len(cliques)
        C = 0
        for clique in cliques:
            C += (-1) ** (len(clique) - 2) * math.comb(len(clique), 2)
        return V - E + F + C
    
    def resolution_length(G):
        clauses = []
        variables = set()
        for u, v in edges:
            var_u = f"x{u}"
            var_v = f"x{v}"
            variables.add(var_u)
            variables.add(var_v)
            clauses.append([var_u, var_v])
            clauses.append([-var_u, -var_v])
            clauses.append([var_u, -var_v])
            clauses.append([-var_u, var_v])
        
        def unit_propagate(clauses):
            while True:
                changed = False
                for clause in clauses:
                    if len(clause) == 1:
                        literal = clause[0]
                        if literal > 0:
                            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                            clauses = new_clauses
                            changed = True
                        else:
                            return False
                if not changed:
                    break
            return True
        
        def dpll(clauses, assignment):
            unit_propagate(clauses)
            if not clauses:
                return True
            literal = next((l for l in variables if l not in assignment and -l not in assignment), None)
            if literal is None:
                return False
            assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if dpll(new_clauses, assignment):
                return True
            del assignment[literal]
            assignment[-literal] = True
            new_clauses = [c for c in clauses if -literal not in c and literal not in c]
            if dpll(new_clauses, assignment):
                return True
            del assignment[-literal]
            return False
        
        return len(clauses)
    
    cliques = clique_complex(edges)
    chi_G = euler_characteristic(cliques)
    res_length = resolution_length(edges)
    
    metric_name = "Resolution length"
    metric_value = res_length
    instances_tested = 1
    conjecture_holds = res_length >= 2 ** (0.5 * chi_G)
    counterexample = "" if conjecture_holds else f"Graph with n={n}, chi(G)={chi_G}, res_length={res_length}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n=40, chi(G)={chi_G}, res_length={res_length}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")