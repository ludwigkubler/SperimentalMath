import sys
import random
from networkx import Graph, DiGraph
from sage.all import MatrixSpace, QQ, ZZ

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
            clauses.append(clause)
        return clauses

    def incidence_graph(clauses):
        G = DiGraph()
        for i, clause in enumerate(clauses):
            for var in clause:
                if var not in G:
                    G.add_node(var)
                G.add_edge(i, abs(var))
        return G

    def grothendieck_group(G):
        nodes = list(G.nodes())
        M = MatrixSpace(QQ, len(nodes), len(nodes))()
        for u, v in G.edges():
            M[u-1, v-1] += 1
            M[v-1, u-1] -= 1
        return M.echelon_form().rank()

    def resolution_width(clauses):
        width = 0
        stack = []
        for clause in clauses:
            new_clause = [abs(var) for var in clause if var not in stack]
            if len(new_clause) > width:
                width = len(new_clause)
            stack.extend([var for var in clause if var not in stack])
        return width

    n_values = [5, 8, 11, 14]
    results = []
    for n in n_values:
        clauses = generate_3sat_instance(n)
        G = incidence_graph(clauses)
        rank_K0 = grothendieck_group(G)
        w_phi = resolution_width(clauses)
        results.append({"n": n, "rank_K0": rank_K0, "w_phi": w_phi})

    max_rank_K0 = max(result["rank_K0"] for result in results)
    min_w_phi = min(result["w_phi"] for result in results)

    if max_rank_K0 > 2 * min_w_phi:
        conjecture_holds = False
        counterexample = f"max(K_0)={max_rank_K0} > 2*min(w)=2*{min_w_phi}"
    else:
        conjecture_holds = True
        counterexample = ""

    return {
        "metric_name": "K-theory rank vs resolution width",
        "metric_value": max_rank_K0,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")