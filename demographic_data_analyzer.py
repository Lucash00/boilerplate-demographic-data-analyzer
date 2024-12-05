import pandas as pd

def calculate_demographic_data(print_data=True):
    # Leer datos del archivo
    df = pd.read_csv('adult.data.csv', header=None)
    df.columns = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 
                  'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 
                  'hours-per-week', 'native-country', 'salary']
    
    # Asegurarse de que las columnas numéricas estén en formato adecuado
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df['capital-gain'] = pd.to_numeric(df['capital-gain'], errors='coerce')
    df['capital-loss'] = pd.to_numeric(df['capital-loss'], errors='coerce')
    df['hours-per-week'] = pd.to_numeric(df['hours-per-week'], errors='coerce')
    
    # Eliminar filas con valores nulos en columnas críticas
    df = df.dropna(subset=['race', 'sex', 'education', 'salary', 'hours-per-week'])

    # Realizar los cálculos
    race_count = df['race'].value_counts()
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)  # Redondear a 1 decimal
    percentage_bachelors = round((df[df['education'] == 'Bachelors'].shape[0] / df.shape[0]) * 100, 1)  # Redondear a 1 decimal
    
    higher_education = df[df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    higher_education_rich = round((higher_education[higher_education['salary'] == '>50K'].shape[0] / higher_education.shape[0]) * 100, 1)  # Redondear a 1 decimal
    
    lower_education = df[~df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    lower_education_rich = round((lower_education[lower_education['salary'] == '>50K'].shape[0] / lower_education.shape[0]) * 100, 1)  # Redondear a 1 decimal
    
    min_work_hours = df['hours-per-week'].min()
    num_min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_percentage = round((num_min_workers[num_min_workers['salary'] == '>50K'].shape[0] / num_min_workers.shape[0]) * 100, 1)  # Redondear a 1 decimal
    
    country_earning = df.groupby('native-country')['salary'].transform(
        lambda x: (x == '>50K').mean() * 100
    )
    country_earning = country_earning.groupby(df['native-country']).first()
    highest_earning_country_percentage = round(country_earning.max(), 1)  # Redondear a 1 decimal
    
    top_IN_occupation = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]['occupation'].mode()[0]

    # Imprimir los resultados si es necesario
    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

