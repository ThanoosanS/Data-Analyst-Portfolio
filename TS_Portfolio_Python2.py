# BMI Calculator using Python

# Gather inputs and cast the height and weight as integers
name = input('Hello! What is your name?:')
height = int(input('What is your height in inches?:'))
weight = int(input('What is your weight in pounds?:'))

bmi = (weight*703)/(height*height)

if bmi > 0:
    if bmi < 18.5:
        print(name + ' you are underweight with minimal risk with a BMI of ' + str(bmi))
    elif (bmi >= 18.5 and bmi <= 24.9):
        print(name + ' you are normal weight with minimal risk with a BMI of ' + str(bmi))
    elif (bmi >= 25 and bmi <= 29.9):
        print(name + ' you are overweight with increased risk with a BMI of ' + str(bmi))
    elif (bmi >= 30 and bmi <= 34.9):
        print(name + ' you are obese with high risk with a BMI of' + str(bmi))
    elif (bmi >= 35 and bmi <= 39.9):
        print(name + ' you are severely obese with very high risk with a BMI of ' + str(bmi))
    else:
        print(name + ' you are morbidly obese with extremely hight risk with a BMI of ' + str(bmi))
else:
    print('invalid')

