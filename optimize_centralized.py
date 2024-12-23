import gurobipy as gp
from gurobipy import GRB
import numpy as np

costs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]  # 0.1*i for i in range(0,11)]
valuations = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
# costs = [np.random.normal(0.5, 0.3) for _ in range(20)]
# valuations = [np.random.uniform(0.5, 0.3) for _ in range(30)]
commission = 0.1

S = len(costs)
B = len(valuations)


## model
m = gp.Model()

x = m.addVars(S, B, vtype=GRB.CONTINUOUS, lb=0, ub=1)
p = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1)
z_s = m.addVars(S, B, vtype=GRB.BINARY)
z_b = m.addVars(S, B, vtype=GRB.BINARY)

M = 1e6

m.setObjective(gp.quicksum(x[s, b] for s in range(S) for b in range(B)) * p * commission, GRB.MAXIMIZE)

for s in range(S):
    for b in range(B):
        m.addConstr(x[s, b] <= 1/(S*B))

        m.addConstr(x[s, b] <= z_s[s, b] * M)
        m.addConstr(x[s, b] <= z_b[s, b] * M)

        m.addConstr(costs[s] - p * (1 - commission) <= M * (1 - z_s[s, b]))
        m.addConstr(p - valuations[b] <= M * (1 - z_b[s, b]))

m.optimize()

print('Price: ', p.x)

def printing():
    print('Price: ', p.x)
    for b in range(B):
        print(f"Buyer {b} with valuation {valuations[b]}")
        print(f"c: {'  | '.join(['%.1f' % round(costs[s],2) for s in range(S)])}")
        print(f"x: {' | '.join(['%.2f' % round(x[s,b].x,2) for s in range(S)])}")



