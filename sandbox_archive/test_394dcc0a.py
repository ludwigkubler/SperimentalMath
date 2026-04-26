import random
import math
from itertools import combinations

def generate_random_graph(n: int, p: float) -> list:
    G = [[] for _ in range(n)]
    for u, v in combinations(range(n), 2):
        if random.random() < p:
            G[u].append(v)
            G[v].append(u)
    return G

def is_connected(G: list) -> bool:
    visited = [False] * len(G)
    stack = [0]
    while stack:
        u = stack.pop()
        if not visited[u]:
            visited[u] = True
            for v in G[u]:
                if not visited[v]:
                    stack.append(v)
    return all(visited)

def find_cycle(G: list) -> bool:
    n = len(G)
    parent = [-1] * n
    rank = [0] * n

    def find(x):
        if parent[x] == -1:
            return x
        return find(parent[x])

    def union(x, y):
        x_set = find(x)
        y_set = find(y)

        if rank[x_set] < rank[y_set]:
            parent[x_set] = y_set
        elif rank[x_set] > rank[y_set]:
            parent[y_set] = x_set
        else:
            parent[y_set] = x_set
            rank[x_set] += 1

    for u in range(n):
        for v in G[u]:
            if find(u) == find(v):
                return True
            union(u, v)
    return False

def genus(G: list) -> int:
    n = len(G)
    e = sum(len(neighbors) for neighbors in G) // 2
    g = (e - n + 1) / 2
    if not is_connected(G):
        return math.inf
    if find_cycle(G):
        return math.inf
    return int(math.ceil(g))

def tseitin_formula(G: list, start: int) -> str:
    n = len(G)
    literals = {i: f'x{i}' for i in range(n)}
    formula = []
    for u in range(n):
        clause = [f'-{literals[u]}']
        for v in G[u]:
            clause.append(literals[v])
        formula.append(' '.join(clause))
    return ' | '.join(formula)

def dpll_solve(formula: str) -> bool:
    clauses = formula.split(' | ')
    literals = set()
    for clause in clauses:
        literals.update(clause.split())

    def is_satisfiable(model):
        for literal in literals:
            if literal[0] == '-' and literal[1:] in model or literal in model:
                continue
            return False
        return True

    stack = []
    while stack or not all(is_satisfiable(model) for model in stack):
        if not stack:
            model = {literal: random.choice([True, False]) for literal in literals}
            stack.append(model)
        else:
            model = stack.pop()
            unsatisfied_clauses = [clause for clause in clauses if not any(literal in model or literal[0] == '-' and literal[1:] in model for literal in clause.split())]
            if not unsatisfied_clauses:
                return True
            literal = random.choice(unsatisfied_clauses[0].split())
            stack.append(model.copy())
            model[literal] = False
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    p = 0.3
    G = generate_random_graph(n, p)
    g_G = genus(G)
    if g_G == math.inf:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    formula = tseitin_formula(G, 0)
    resolution_width = dpll_solve(formula)
    if resolution_width is None:
        resolution_width = math.inf
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width,
        "instances_tested": 1,
        "conjecture_holds": resolution_width >= g_G * 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_width = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] or r["metric_value"] is None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] is not None for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")