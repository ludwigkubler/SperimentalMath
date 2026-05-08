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
    def generate_3_regular_graph(n):
        while True:
            edges = set()
            for i in range(n):
                neighbors = random.sample(range(n), 2)
                if (i, neighbors[0]) not in edges and (neighbors[0], i) not in edges:
                    edges.add((i, neighbors[0]))
                    edges.add((i, neighbors[1]))
            if len(edges) == n * 3 // 2:
                return [set() for _ in range(n)], list(edges)

    def union_find(n):
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            rootX = find(x)
            rootY = find(y)
            if rootX != rootY:
                if rank[rootX] > rank[rootY]:
                    parent[rootY] = rootX
                elif rank[rootX] < rank[rootY]:
                    parent[rootX] = rootY
                else:
                    parent[rootY] = rootX
                    rank[rootX] += 1

        return find, union

    def percolation(G, p):
        n = len(G)
        uf, _ = union_find(n)
        for u in range(n):
            for v in G[u]:
                if random.random() < p:
                    uf(u, v)
        components = set()
        for i in range(n):
            components.add(uf(i))
        return len(components) == 1

    def tseitin_formula(G, sigma):
        n = len(G)
        clauses = []
        variables = {}
        var_id = 0
        for u in range(n):
            for v in G[u]:
                if (u, v) not in variables:
                    variables[(u, v)] = var_id
                    var_id += 1
                clauses.append([variables[(u, v)], -variables[(v, u)]])
        return clauses

    def tree_dpll(clauses, model):
        def dpll(clauses, model):
            if not clauses:
                return True
            unit_clauses = [c for c in clauses if len(c) == 1]
            if unit_clauses:
                literal = unit_clauses[0][0]
                if literal < 0:
                    literal = -literal
                    polarity = False
                else:
                    polarity = True
                model[literal] = polarity
                new_clauses = []
                for c in clauses:
                    if literal not in c and -literal not in c:
                        new_clauses.append(c)
                return dpll(new_clauses, model)
            pure_literals = [l for l in range(1, max(model.keys()) + 1) if all(l not in c or -l not in c for c in clauses)]
            if pure_literals:
                literal = pure_literals[0]
                polarity = True
                model[literal] = polarity
                new_clauses = []
                for c in clauses:
                    if literal not in c and -literal not in c:
                        new_clauses.append(c)
                return dpll(new_clauses, model)
            literal = random.choice([l for l in range(1, max(model.keys()) + 1)])
            polarity = True
            model[literal] = polarity
            new_clauses = []
            for c in clauses:
                if literal not in c and -literal not in c:
                    new_clauses.append(c)
            return dpll(new_clauses, model) or dpll(clauses, {k: not v for k, v in model.items()})

        return dpll(clauses, {})

    def reliability_deficit(G):
        n = len(G)
        p = 0.5
        R_hat = sum(percolation(G, p) for _ in range(5000)) / 5000
        if R_hat < 1/5000:
            R_hat = 1/5000
        return -math.log2(1 - R_hat)

    def tseitin_reliability(G):
        clauses = tseitin_formula(G, {})
        return tree_dpll(clauses, {})

    n_values = [12, 20, 28, 36, 40]
    results = []
    for n in n_values:
        G_expander, _ = generate_3_regular_graph(n)
        G_non_expander = [[(i, (i + j) % n) for j in range(1, 3)] for i in range(n)]
        G_non_expander = sum(G_non_expander, [])
        G_non_expander = [set() for _ in range(n)] + G_non_expander
        for G in [G_expander, G_non_expander]:
            ν_G = reliability_deficit(G)
            log_L_R = tseitin_reliability(G)
            results.append({
                "n": n,
                "G_type": "expander" if G == G_expander else "non-expander",
                "ν_G": ν_G,
                "log_L_R": log_L_R
            })

    ρ = 0.7
    support_fraction = 0
    for result in results:
        n, G_type, ν_G, log_L_R = result["n"], result["G_type"], result["ν_G"], result["log_L_R"]
        if G_type == "expander":
            if ν_G >= 6 and log_L_R < ν_G / 16:
                return {"seed": seed, "metric_name": "ρ", "metric_value": ρ, "instances_tested": len(results), "conjecture_holds": False, "counterexample": f"expander with ν_G={ν_G} and log_L_R={log_L_R}"}
        else:
            if ν_G < 6 or log_L_R > 16 * ν_G * math.log2(n):
                return {"seed": seed, "metric_name": "ρ", "metric_value": ρ, "instances_tested": len(results), "conjecture_holds": False, "counterexample": f"non-expander with ν_G={ν_G} and log_L_R={log_L_R}"}
        if G_type == "expander":
            support_fraction += 1

    return {"seed": seed, "metric_name": "ρ", "metric_value": ρ, "instances_tested": len(results), "conjecture_holds": support_fraction / len(results) >= ρ, "counterexample": ""}

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")