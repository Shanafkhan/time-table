import pandas as pd
import itertools

def generate_timetable(subjects, teachers_mapping, start_time, end_time, lecture_hours, break_after_hours, break_duration, lunch_start, lunch_duration, num_weeks):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)
    lunch_start = pd.to_datetime(lunch_start)

    timetable_data = {'Day': [], 'Time': [], 'Subject': [], 'Teacher': []}

    for day in days:
        current_time = start_time
        subject_count = 0
        lecture_count = 0

        while current_time < end_time:
            if current_time.time() == lunch_start.time():
                current_time += pd.Timedelta(minutes=lunch_duration)
                timetable_data['Day'].append(day)
                timetable_data['Time'].append(current_time.strftime('%H:%M'))
                timetable_data['Subject'].append('Lunch')
                timetable_data['Teacher'].append('Lunch')
            else:
                if lecture_count % (break_after_hours * len(subjects)) == 0 and lecture_count != 0:
                    current_time += pd.Timedelta(minutes=break_duration)
                    timetable_data['Day'].append(day)
                    timetable_data['Time'].append(current_time.strftime('%H:%M'))
                    timetable_data['Subject'].append('Break')
                    timetable_data['Teacher'].append('Break')
                else:
                    subject = subjects[subject_count % len(subjects)]
                    teacher = teachers_mapping[subject]
                    
                    timetable_data['Day'].append(day)
                    timetable_data['Time'].append(current_time.strftime('%H:%M'))
                    timetable_data['Subject'].append(f'{subject} - {teacher}')
                    timetable_data['Teacher'].append(teacher)

                    for _ in range(lecture_hours):
                        current_time += pd.Timedelta(hours=1)
                        timetable_data['Day'].append(day)
                        timetable_data['Time'].append(current_time.strftime('%H:%M'))
                        timetable_data['Subject'].append(f'{subject} - {teacher}')
                        timetable_data['Teacher'].append(teacher)

                    subject_count += 1
                    lecture_count += 1

    df = pd.DataFrame(timetable_data)
    return df

def pivot_timetable(timetable):
    pivoted_timetable = timetable.pivot_table(index=['Day'], columns='Time', values='Subject', aggfunc='first')
    return pivoted_timetable

def export_to_excel(dataframe, filename='timetable.xlsx'):
    dataframe.to_excel(filename)
    print(f'Timetable exported to {filename}')

if __name__ == "__main__":
    #subjects = ['Math', 'Science', 'History', 'English', 'Physical Education']
    #teachers_mapping = {'Math': 'Teacher 1', 'Science': 'Teacher 2', 'History': 'Teacher 3', 'English': 'Teacher 1', 'Physical Education': 'Teacher 2'}
    #start_time = '10:00'
    #end_time = '17:00'
    #lecture_hours = 1
    break_after_hours = 3
    break_duration = 15
    #lunch_start = '13:00'
    #lunch_duration = 60
    num_weeks = 1  # Set to 1 week

    #timetable = generate_timetable(subjects, teachers_mapping, start_time, end_time, lecture_hours, break_after_hours, break_duration, lunch_start, lunch_duration, num_weeks)
    #pivoted_timetable = pivot_timetable(timetable)
    #export_to_excel(pivoted_timetable)
