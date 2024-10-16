import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Union


def filter_data(df: pd.DataFrame, semester: str=None, subject: str=None,
                date: str=None, grade: str=None) -> Union[pd.DataFrame, None]:
    """Filters data by a specific subject, semester, grade, or limit by date."""

    def validate_data(data: str) -> Union[tuple, None]:
        """Validates the input data."""
        data = [i.strip().replace(',', '.') for i in data.split(' ')]
        # try:
        if len(data) > 2:
            raise ValueError('Too many values.')

        elif len(data) == 1:
            if data[0].replace('.', '', 1).isdigit():
                data[0] = float(data[0])
            else:
                data[0] = pd.to_datetime(data[0], errors='raise')
            return tuple(data)

        else:
            greater_than = None
            if data[0].replace('.', '', 1).isdigit():
                data[0] = float(data[0])
            elif data[0] in '><':
                greater_than = True if data[0] == '>' else False
            elif pd.to_datetime(data[0], errors='raise') is not pd.NaT:
                data[0] = pd.to_datetime(data[0])
            else:
                raise ValueError('Invalid first value.')

            if data[1].replace('.', '', 1).isdigit():
                data[1] = float(data[1])
            elif data[1] in '><':
                if greater_than:
                    raise ValueError('Not enough numbers.')
                greater_than = True if data[1] == '<' else False
            elif pd.to_datetime(data[1], errors='raise') is not pd.NaT:
                data[1] = pd.to_datetime(data[1])

            if greater_than:
                value = data[0] if data[0] not in '><' else data[1]
                return value, '+' if greater_than else '-'
            else:
                return min(data), max(data)

        # except Exception as e:
        #     print(e)
        #     return None

    def filter_df_column(df_main: pd.DataFrame, data: tuple, column_name: str) -> Union[pd.DataFrame, None]:
        """Filters a DataFrame by a specific column."""
        if len(data) == 1:
            df_main = df_main[df_main[column_name] == data[0]]
            return df_main
        elif len(data) == 2:
            if data[1] == '+' or data[1] == '-':
                if data[1] == '+':
                    df_main = df_main[df_main[column_name] > data[0]]
                else:
                    df_main = df_main[df_main[column_name] < data[0]]
            else:
                df_main = df_main[(df_main[column_name] >= data[0]) & (df_main[column_name] <= data[1])]
        else:
            raise ValueError('Invalid data.')
        return df_main
    if subject:
        try:
            subject_cleaned = [i.strip().lower() for i in subject.split(' ')]
            df = df[df['Subject'].str.lower().isin(subject_cleaned)]
        except Exception as e:
            print('Subject error\n', e)
    if semester:
        try:
            semester_cleaned = validate_data(semester)
            df = filter_df_column(df, semester_cleaned, 'Semester')
        except Exception as e:
            print('Semester error\n', e)
    if date:
        try:
            date_cleaned = validate_data(date)
            df = filter_df_column(df, date_cleaned, 'Date')
        except Exception as e:
            print('Date error\n', e)
    if grade:
        try:
            grade_cleaned = validate_data(grade)
            df = filter_df_column(df, grade_cleaned, 'Grade')
        except Exception as e:
            print('Grade error\n', e)
    return df

def show_info(df: pd.DataFrame) -> int:
    """Shows basic info about the DataFrame."""
    print(df.describe().loc[['count', 'mean', 'min', '25%', '50%', '75%', 'max']])
    return 0

def plot_grades_bar_distribution(df: pd.DataFrame) -> int:
    """Plots a bar distribution of grades with count labels above each bar."""
    grade_counts = df['Grade'].value_counts().reindex(np.arange(2, 5.5, 0.5), fill_value=0)

    plt.figure(figsize=(14, 7))
    bars = plt.bar(np.arange(2, 5.5, 0.5), grade_counts.values, color='#4C72B0', alpha=0.8, edgecolor='black',
                   width=0.4)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}',
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

    plt.xlabel('Grade', fontsize=12, fontweight='bold')
    plt.ylabel('Frequency', fontsize=12, fontweight='bold')
    plt.title('Grade Distribution', fontsize=15, fontweight='bold', color='#4C72B0')
    plt.xticks(ticks=np.arange(2, 5.5, 0.5))
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()
    return 0

def plot_avg_grade_per_semester(df: pd.DataFrame) -> int:
    """Plots the average grade per semester with confidence intervals."""
    sns.set_theme(style="whitegrid")
    avg_grades = df.groupby('Semester')['Grade'].agg(['mean', 'std']).reset_index()

    plt.figure(figsize=(10, 6))
    plt.errorbar(avg_grades['Semester'], avg_grades['mean'], yerr=avg_grades['std'],
                 fmt='-o', color='#55A868', ecolor='gray', capsize=5, capthick=1, markersize=6)

    for i in range(len(avg_grades)):
        plt.text(avg_grades['Semester'][i], avg_grades['mean'][i] + 0.05,
                 f'{avg_grades["mean"][i]:.2f}', ha='center', va='bottom',
                 fontsize=10, fontweight='bold', color='black')

    plt.xlabel('Semester', fontsize=12, fontweight='bold')
    plt.xticks(ticks=avg_grades['Semester'].astype(int))
    plt.ylabel('Average Grade', fontsize=12, fontweight='bold')
    plt.yticks(ticks=np.arange(2, 5.5, 0.5))
    plt.title('Average Grade per Semester', fontsize=15, fontweight='bold', color='#55A868')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()
    return 0

def close_plots() -> int:
    """Closes all open plots."""
    plt.close('all')
    return 0
