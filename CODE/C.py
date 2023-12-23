import socket

def snd_cmd(cl_socket, cmd):

    # Send a command to the server and receive the response.
    cl_socket.send(cmd.encode())
    res = cl_socket.recv(1024).decode()
    return res

def main():

    # Main function for the HR System client.
    host = 'localhost'
    port = 8888

    cl_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cl_s.connect((host, port))

    print("HR System 1.0")

    while True:

        # Query employee ID
        employee_id = input("What is the employee id? ")

        res = snd_cmd(cl_s, f'VERIFY,{employee_id}')
        print("Server response:", res)

        if res == 'NOT RECOGNIZED':
            print("Please try again, 'Employee ID not recognized'.")
            continue

        # Query salary or annual leave
        command = input("Salary (S) or Annual Leave (L) Query? ")
        cmd = ''
        if command == 'S':
            # Query salary details
            s_type = input("Current salary (C) or total salary (T) for year? ")
            if s_type == 'C':
                cmd = 'CSALARY,' + employee_id
            elif s_type == 'T':
                year = input("For which year? ")
                cmd = 'TSALARY,' + employee_id + ',' + year
        elif command == 'L':
            # Query annual leave details
            l_type = input("Current Entitlement (C) or Leave taken for year (Y)? ")
            if l_type == 'C':
                cmd = 'CENTITLE,' + employee_id
            elif l_type == 'Y':
                year = input("For which year? ")
                cmd = 'YTAKEN,' + employee_id + ',' + year
        elif command == 'C':
            cmd = 'CONTINUE'

        # Send the command to the server and print the response
        res = snd_cmd(cl_s, cmd)
        print(res)

        # Ask user if they want to continue or exit
        choice = input("Would you like to continue (C) or exit (X)? ")
        if choice.upper() == 'X':

            # Send exit command to the server and break out of the loop
            cl_s.send('EXIT'.encode())
            break
        elif choice.upper() != 'C':
            print("sorry! Invalid choice, Please enter 'C' or 'X' only.")
            break

    # Close the client socket and print farewell message
    cl_s.close()
    print("Goodbye!")

if __name__ == "__main__":
    main()