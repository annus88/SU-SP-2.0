def calculate_gpa(grades):

    total_points = 0

    count = 0

    mapping = {

        "A+":4.0,
        "A":4.0,
        "B+":3.5,
        "B":3.0,
        "C+":2.5,
        "C":2.0,
        "D":1.0,
        "F":0.0

    }

    for grade in grades:

        total_points += mapping.get(
            grade.grade,
            0
        )

        count += 1

    if count == 0:
        return 0

    return round(
        total_points / count,
        2
    )