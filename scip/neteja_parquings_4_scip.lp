Minimize
 obj: d1*x01 + d*2x2 + 3 x3 + x4
Subject To
 c1_lower: - x1 + x2 + x3 + 10 x4 >= 0
 c1_upper: - x1 + x2 + x3 + 10 x4 <= 20
 c2: x1 - 3 x2 + x3 <= 30
 c3: x2 - 3.5 x4 = 0
Bounds
 0 <= x1 <= 40
 2 <= x4 <= 3
General
 x01
 x2
 x3
 x4
End