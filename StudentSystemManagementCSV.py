import csv

# Variable storing the path to the .csv file
filePath = ""

# Function to retrieve the last ID from the file
def get_last_id(file_path):
    try:
        # Open the .csv file for reading
        with open(file_path, 'r') as csv_file:
            # Create a CSV reader
            reader = csv.reader(csv_file)

            # Iterate through all rows to reach the last one
            for row in reader:
                pass

            # If the row exists, get the last ID as an integer; otherwise, set it to 0
            if row:
                last_id = int(row[0])
            else:
                last_id = 0
        return last_id
    except FileNotFoundError:
        # Handle the exception when the file does not exist
        return 0

# Function to find a free ID
def find_free_id(data):
    # Create a set of occupied IDs, skipping the first row with headers
    occupied_ids = set()
    for student in data[1:]:
        student_id = int(student[0])
        occupied_ids.add(student_id)

    new_id = 1
    # Search for the first free ID, starting from 1
    while new_id in occupied_ids:
        new_id += 1
    return new_id

# Function to add a new student
def add_new_student(file_path, new_student_data):
    # Read existing data from the .csv file
    with open(file_path, "r") as file:
        data = list(csv.reader(file, delimiter=","))

    # Add a new student with an automatically assigned ID
    with open(file_path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        new_id = find_free_id(data)
        writer.writerow([new_id] + new_student_data)

    # Read data after adding the new student
    with open(file_path, 'r') as csv_file:
        data = list(csv.reader(csv_file))

    # Sort data by ID (skip the first row containing headers)
    data_sorted = sorted(data[1:], key=lambda x: int(x[0]))

    # Write the sorted data back to the file
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["ID", "FIRST_NAME", "LAST_NAME", "STUDENT_NUMBER"])  # Add headers
        writer.writerows(data_sorted)

while True:
    print("[==================[STUDENT DATABASE]=================]")
    print("1. Create a file")
    print("2. Add a student")
    print("3. Remove a student")
    print("4. Display student database")
    print("5. Load a file")
    print("6. Exit")
    print("===========[---------------------]===========")
    menu_option = input("Choose an option [1-6]: ")

    match menu_option:
        case "1":
            # Check if the file path has been loaded or created before
            if filePath != "":
                print(f"A .csv file with the student database has already been created or loaded from the path:\n{filePath}")
                choose_option = input("If you want to create a new file, enter 'T' and choose option 1 from the menu again.\nIf not, enter 'N' and continue working with the existing file: ")
                if choose_option == "T":
                    filePath = ""
                elif choose_option == "N":
                    print(f"You are working with the file: {filePath}")
                else:
                    print("Incorrect value entered!")
            else:
                print("Creating a new .csv file...")

                # Enter column headers
                headers = ['ID', 'FIRST_NAME', 'LAST_NAME', 'STUDENT_NUMBER']

                # Enter the path to the folder and file name
                filePath = input("Enter the path to the folder along with the file name where the file should be saved (e.g., C:\\Users\[username]\Desktop\students.csv): ")

                try:
                    # Open a new .csv file for writing
                    with open(filePath, 'w', newline='') as file:
                        # Create an object for writing to the .csv file
                        writer = csv.writer(file)

                        # Write column headers to the file
                        writer.writerow(headers)
                        print("The .csv file has been created at the specified path.")
                except PermissionError:
                    # Error message when there are no permissions to write in the selected location
                    print("Error: Lack of permissions to write in the selected location. Run the program as an administrator or choose a different location for the .csv file.")
                except Exception as e:
                    # General error message
                    print(f"Error: {e}")
        case "2":
            # Check if the file path has been loaded or created before
            if filePath == "":
                print("First, load the .csv file with the student database or create one!")
            else:
                print("Adding a student to the database...")

                # Enter data for a new student
                new_student = input("Enter student data according to the pattern (First Name,Last Name,Student Number): ")
                new_student_data = new_student.split(',')

                # Add a new student with an automatically assigned ID
                add_new_student(filePath, new_student_data)

                print("A new student has been added to the CSV file.")
        case "3":
            # Check if the file path has been loaded or created before
            if filePath == "":
                print("First, load the .csv file with the student database or create one!")
            else:
                # List to store rows from the .csv file
                lines = list()

                # Enter the ID of the student to be removed from the database
                student_id = input("Enter the ID of the student to be removed from the database: ")

                # Open the .csv file for reading
                with open(f'{filePath}', 'r') as read_file:
                    # Create an object for reading the .csv file
                    reader = csv.reader(read_file)

                    # Loop iterating through the rows in the .csv file
                    for row in reader:
                        # Save rows from the file to the list
                        lines.append(row)

                        # Loop iterating through the fields in a given row
                        for field in row:
                            # Check if the ID in a given field is equal to the entered ID
                            if field == student_id:
                                # Remove the entire row from the list if the ID matches
                                lines.remove(row)

                # Open the .csv file for writing
                with open(f'{filePath}', 'w', newline='') as write_file:
                    # Create an object for writing to the .csv file
                    writer = csv.writer(write_file)

                    # Save the updated list of rows to the .csv file
                    writer.writerows(lines)

                print(f"The student with ID: {student_id} has been removed from the database.")
        case "4":
            # Message about starting to display the list of students
            print("[====================[STUDENT LIST]====================]")

            # Check if the file path has been loaded or created
            if filePath == "":
                # Message about the need to load or create a .csv file
                print("First, load the .csv file with the student database or create one!")
            else:
                # Open the .csv file
                file = open(f"{filePath}", "r")

                # Assign data from the .csv file to a list
                data = list(csv.reader(file, delimiter=","))

                # Close the .csv file after reading the data
                file.close()

                # Check if there is data in the database
                if len(data) > 0:
                    # Column headers
                    print("{:<15} {:<15} {:<15} {:<15}".format(data[0][0], data[0][1], data[0][2], data[0][3]))
                    # Separating line
                    print("-" * 60)

                    # Loop iterating through rows of data (skipping the first row with headers)
                    for i in range(1, len(data)):
                        # Rows with data
                        print("{:<15} {:<15} {:<15} {:<15}".format(data[i][0], data[i][1], data[i][2], data[i][3]))

                    # Separating line
                    print("-" * 60)
                else:
                    # Message about the lack of data to display
                    print("No data to display.")
        case "5":
            # Message about starting to load data from the .csv file
            print("Loading data from the .csv file")
            # Enter the path to the .csv file from the user
            filePath = input("Enter the path to the .csv file (e.g., C:\\students.csv): ")
            # Replace any '\' characters with '\\'
            filePath = filePath.replace("\'", "\\")
            # Message about completing the data loading
            print("The .csv file with data has been loaded. Now you can work with it.")
        case "6":
            print("Exiting the program...")
            break
        case _:
            print("There is no such option, choose again!")
