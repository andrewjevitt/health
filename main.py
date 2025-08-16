from math import log

FAT_TO_CALORIES = 3500  # lb to Cal (or kcal)
LB_TO_KG = 0.4535924
FEET_TO_METERS = 0.3048
CAL_PER_CARB_G = 4
CAL_PER_FAT_G = 9
CAL_PER_PROTEIN_G = 4
PROTEIN_FOR_MUSCLE = 1  # gram per pound lean mass, post workout
CAL_PER_SIRLOIN_OZ = 55 #  cooked sirloin beef

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
    return f"{0.5*weight:0.0f}-{1*weight} oz"


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

def burn_calories(caloric_deficit, mode="walk"):
    """
    Calculate how many miles you need to walk, run, or bike to burn a given caloric deficit.

    Parameters:
    - caloric_deficit (float): The number of calories to burn.
    - mode (str): Activity mode, one of "walk", "run", or "bike".

    Returns:
    - float: Estimated number of miles needed.
    """
    # Average calories burned per mile for a person around 155–160 lbs
    burn_rates_per_mile = {
        "walk": 90,   # calories per mile
        "run": 120,   # calories per mile
        "bike": 45    # calories per mile
    }

    mode = mode.lower()
    if mode not in burn_rates_per_mile:
        raise ValueError(f"Unsupported mode '{mode}'. Choose from: {list(burn_rates_per_mile.keys())}")
    if caloric_deficit <= 0:
        raise ValueError("Caloric deficit must be a positive number.")

    miles_needed = caloric_deficit / burn_rates_per_mile[mode]
    return round(miles_needed, 2)

# 5'10 -> BI "healthy" weight is 167 max down to 132.


def main():
    height = 5 + 10 / 12  # feet
    weight = 230  # LB
    age = 31
    BMR = basal_metabolic_rate(weight * LB_TO_KG, height * FEET_TO_METERS * 100, age)
    BMI = body_mass_index(weight * LB_TO_KG, height * FEET_TO_METERS)
    print(f"BMR: {BMR:0.1f} calories at rest")
    print(f"BMI: {BMI:0.1f} {"overweight" if BMI > 25 else "Normal/Underweight"}")
    print(f"Daily water intake {daily_water_intake(weight)}")

    weight_per_period = float(input("How much weight in pounds do you want to lose? "))
    time_frame = float(input("Over how many weeks? "))
    pounds_per_week = weight_per_period/time_frame
    print(f"You are aiming to lose {pounds_per_week:0.1f} pounds each week for {time_frame} weeks.")
    print(f"This equates to {pounds_per_week*FAT_TO_CALORIES:0.0f} calorie deficit per week.")
    daily_deficit = pounds_per_week*FAT_TO_CALORIES/7
    print(f"You must achieve a daily caloric defit of {daily_deficit:0.0f}")
    print(f"If you do not change your diet this means you need to add ")
    print(f"Walk {burn_calories(daily_deficit, 'walk')} miles, {burn_calories(daily_deficit, 'walk')*15/60:0.1f} hr a day")
    print(f"Run {burn_calories(daily_deficit, 'run')} miles, {burn_calories(daily_deficit, 'run')*12/60:0.1f} hr a day")
    print(f"Bike {burn_calories(daily_deficit, 'bike')} miles, {burn_calories(daily_deficit, 'bike')*6/60:0.1f} hr a day")

    print(f"With this, you would be at {weight-weight_per_period} lbs -> BMI {body_mass_index((weight-weight_per_period) * LB_TO_KG, height * FEET_TO_METERS):0.1f} {"overweight" if body_mass_index((weight-weight_per_period) * LB_TO_KG, height * FEET_TO_METERS) > 25 else "Normal/Underweight"}")

    print(f"Assuming you want to bike only 1 mile per day, you need to cut out {(burn_calories(daily_deficit, 'bike')-1)*daily_deficit/burn_calories(daily_deficit, 'bike'):0.0f} calories")


    print(f"At a base rate, the minimum you should eat to maintain weight would be {BMR/CAL_PER_SIRLOIN_OZ:0.1f} oz of sirloin steak per day.")

    
    # print(f"Bicep Curl 1-rep max {one_rep_max(55+20,30)} lb")

if __name__ == "__main__":
    main()
