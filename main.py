from math import log

FAT_TO_CALORIES = 1 / 3500  # lb to Cal (or kcal)
LB_TO_KG = 0.4535924
FEET_TO_METERS = 0.3048
CAL_PER_CARB_G = 4
CAL_PER_FAT_G = 9
CAL_PER_PROTEIN_G = 4
PROTEIN_FOR_MUSCLE = 1  # gram per pound lean mass, post workout


def body_mass_index(weight, height):
    """Weight kg and height m"""
    return weight / height / height


def basal_metabolic_rate(weight, height, age, gender="male"):
    """Weight kg and height cm, age years"""
    if gender == "male":
        FACTOR = 5
    else:
        FACTOR = -161
    return 10 * weight + 6.25 * height - 5 * age + FACTOR


def target_heart_rate(age, intensity):
    return (220 - age) * intensity


def daily_water_intake(weight):
    """Weight in lb"""
    return f"{0.5*weight}-{1*weight} oz"


def calorie_deficit(desired_lb_per_week, deficit=1000):
    """Pounds per week lost if defict of calories maintained."""
    return desired_lb_per_week * deficit


def body_fat_percent(waist, neck, height, hip=0, gender="male"):
    """Measurements in cm"""
    if gender == "male":
        middle = 1.0324 - 0.19077 * log(waist + hip - neck) + 0.15456 * log(height)
    else:
        assert hip != 0, "Women have hips, so provide a hip measure."
        middle = 1.29579 - 0.35004 * log(waist + hip - neck) + 0.22100 * log(height)
    return 495 / middle - 450


def vo2_max(distance_in_twelve_min):
    return (distance_in_twelve_min - 504.9) / 44.73


def one_rep_max(weight, reps):
    """Hypertrophy typicall 0.6-0.8 one rep max"""
    return weight * (1 + (reps / 30))


def main():
    height = 5 + 10 / 12  # feet
    weight = 230  # LB
    age = 31
    BMR = basal_metabolic_rate(weight * LB_TO_KG, height * FEET_TO_METERS / 100, age)
    BMI = body_mass_index(weight * LB_TO_KG, height * FEET_TO_METERS)
    print(f"BMR: {BMR:0.1f} calories at rest")
    print(f"BMI: {BMI:0.1f} {"overweight" if BMI > 25 else "Normal/Underweight"}")


if __name__ == "__main__":
    main()
