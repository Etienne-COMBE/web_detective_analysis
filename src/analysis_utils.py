import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns

def indicators(series: pd.Series):
    if series.dtype == 'int64' or series.dtype == 'float64':
        print('mean : \t', series.mean())
        print('std : \t', series.std())
        print('median :', series.median())
        print('iqr: \t', series.quantile(0.75) - series.quantile(0.25))
    print('mode :\t', series.mode().values)
    return

def lorenz(series: pd.Series, title,  gini: bool = True):
    lorenz = np.cumsum(np.sort(series)) / np.sum(series)
    lorenz = np.append([0], lorenz)
    n = len(lorenz)
    norm_index = np.arange(n) / n
    plt.title(title)
    sns.lineplot(norm_index, lorenz)
    sns.lineplot(norm_index, norm_index)
    if gini:
        gini_score = 1 - (2 * lorenz.sum()/n)
        plt.fill_between(norm_index, norm_index, lorenz, label = f'Gini score : {gini_score}', color = 'green', alpha = 0.5)
    
    plt.legend()

def feature_time_series(fusion: pd.DataFrame):
    fusion['date'] = pd.to_datetime(fusion['date'])
    fusion['hour'] = fusion['date'].dt.hour
    fusion['date_day'] = fusion['date'].dt.date
    fusion['day'] = fusion['date'].dt.day
    fusion['month'] = fusion['date'].dt.month
    return fusion

def plot_categ_time(fusion: pd.DataFrame):
    sales_by_day = fusion.groupby('date_day')['date_day'].count()
    categ_0 = fusion[fusion['categ'] == '0']
    categ_1 = fusion[fusion['categ'] == '1']
    categ_2 = fusion[fusion['categ'] == '2']
    categ_0_time = categ_0.groupby('date_day')['date_day'].count()
    categ_1_time = categ_1.groupby('date_day')['date_day'].count()
    categ_2_time = categ_2.groupby('date_day')['date_day'].count()

    sns.lineplot(data = sales_by_day, label = 'Total')
    sns.lineplot(data = categ_0_time, label = "categ 0")
    sns.lineplot(data = categ_1_time, label = "categ 1")
    sns.lineplot(data = categ_2_time, label = "categ 2")

def ommit_october(fusion: pd.DataFrame) -> pd.DataFrame:
    before = fusion['date_day'] < pd.to_datetime('2021-10-01')
    after = fusion['date_day'] > pd.to_datetime('2021-10-27')
    ommit_fusion = fusion[before | after]
    return ommit_fusion

def habits_hour_sex(ommit_fusion: pd.DataFrame):
    f_ommit = ommit_fusion[ommit_fusion['sex'] == 'f']
    m_ommit = ommit_fusion[ommit_fusion['sex'] == 'm']
    f_by_hour = f_ommit.groupby('hour')['date'].count() / len(f_ommit)
    m_by_hour = m_ommit.groupby('hour')['date'].count() / len(m_ommit)
    sns.lineplot(data = f_by_hour, label = 'female')
    sns.lineplot(data = m_by_hour, label = 'male')

def habits_day_sex(ommit_fusion: pd.DataFrame):
    f_ommit = ommit_fusion[ommit_fusion['sex'] == 'f']
    m_ommit = ommit_fusion[ommit_fusion['sex'] == 'm']
    f_by_day = f_ommit.groupby('day')['date'].count() / len(f_ommit)
    m_by_day = m_ommit.groupby('day')['date'].count() / len(m_ommit)
    sns.lineplot(data = f_by_day, label = 'female')
    sns.lineplot(data = m_by_day, label = 'male')

def habits_hours_age(ommit_fusion: pd.DataFrame):
    age = datetime.date.today().year - ommit_fusion['birth']
    ommit_junior = ommit_fusion[age < 30]
    ommit_adult = ommit_fusion[(age >= 30) & (age <50)]
    ommit_senior = ommit_fusion[age >= 50]

    junior_by_hour = ommit_junior.groupby('hour')['date'].count() / len(ommit_junior)
    sns.lineplot(data = junior_by_hour, label = 'junior')
    adult_by_hour = ommit_adult.groupby('hour')['date'].count() / len(ommit_adult)
    sns.lineplot(data = adult_by_hour, label = 'adult')
    senior_by_hour = ommit_senior.groupby('hour')['date'].count() / len(ommit_senior)
    sns.lineplot(data = senior_by_hour, label = 'senior')

def habits_day_age(ommit_fusion: pd.DataFrame):
    age = datetime.date.today().year - ommit_fusion['birth']
    ommit_junior = ommit_fusion[age < 30]
    ommit_adult = ommit_fusion[(age >= 30) & (age <50)]
    ommit_senior = ommit_fusion[age >= 50]

    junior_by_day = ommit_junior.groupby('day')['date'].count() / len(ommit_junior)
    sns.lineplot(data = junior_by_day, label = 'junior')
    adult_by_day = ommit_adult.groupby('day')['date'].count() / len(ommit_adult)
    sns.lineplot(data = adult_by_day, label = 'adult')
    senior_by_day = ommit_senior.groupby('day')['date'].count() / len(ommit_senior)
    sns.lineplot(data = senior_by_day, label = 'senior')