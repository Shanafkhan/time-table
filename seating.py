import mysql.connector
from openpyxl import Workbook
import itertools

# Connect to MySQL database
def connect_to_database():
    connection = mysql.connector.connect(
        host="localhost",
        user="username",
        password="password",
        database="students"
    )
    return connection

# Retrieve list of student USNs and branch information from database
def retrieve_student_data(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT usn, branch FROM students_table")
    student_data = cursor.fetchall()
    cursor.close()
    return student_data

# Calculate number of students for each branch
def calculate_students_per_branch(student_data):
    students_per_branch = {}
    for usn, branch in student_data:
        if branch not in students_per_branch:
            students_per_branch[branch] = []
        students_per_branch[branch].append(usn)
    return students_per_branch

# Generate seating arrangement
def generate_seating_arrangement(students_per_branch, num_rooms, num_benches_per_room):
    seating_arrangement = []
    room_number = 1
    all_branch_combinations = itertools.combinations(students_per_branch.keys(), 2)
    for branch1, branch2 in all_branch_combinations:
        students_branch1 = students_per_branch[branch1]
        students_branch2 = students_per_branch[branch2]
        for i in range(0, len(students_branch1), 2):
            table = {
                "room_number": room_number,
                "branch1": branch1,
                "branch2": branch2,
                "usn1": students_branch1[i],
                "usn2": students_branch2[i] if i < len(students_branch2) else None
            }
            seating_arrangement.append(table)
            if len(seating_arrangement) % num_benches_per_room == 0:
                room_number += 1
    return seating_arrangement

# Export seating arrangement to Excel spreadsheet
def export_to_excel(seating_arrangement):
    wb = Workbook()
    ws = wb.active
    ws.append(["USN1", "USN2 (if applicable)", "Room/Block Number"])
    for table in seating_arrangement:
        ws.append([table["usn1"], table["usn2"], table["room_number"]])
    wb.save("seating_arrangement.xlsx")

def main():
    # Connect to database
    connection = connect_to_database()

    # Retrieve student data
    student_data = retrieve_student_data(connection)

    # Calculate number of students for each branch
    students_per_branch = calculate_students_per_branch(student_data)

    # Determine number of rooms needed based on total students and benches per room
    num_rooms = 5  # Change this value according to your requirement
    num_benches_per_room = 2  # Change this value according to your requirement

    # Generate seating arrangement
    seating_arrangement = generate_seating_arrangement(students_per_branch, num_rooms, num_benches_per_room)

    # Export seating arrangement to Excel
    export_to_excel(seating_arrangement)

    # Close database connection
    connection.close()

if __name__ == "__main__":
    main()
