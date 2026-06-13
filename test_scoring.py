from scoring import calculate_points

print(
    "2-1 vs 2-1 =",
    calculate_points(
        2,1,
        2,1
    )
)

print(
    "3-1 vs 2-0 =",
    calculate_points(
        3,1,
        2,0
    )
)

print(
    "1-1 vs 0-0 =",
    calculate_points(
        1,1,
        0,0
    )
)

print(
    "1-0 vs 0-2 =",
    calculate_points(
        1,0,
        0,2
    )
)
