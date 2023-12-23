import sys
sys.stdout = sys.stderr
import socket
import threading
import pika

# Employee data stored in-memory

employees = {
    'E00123': {'Name': 'Laiba Asif', 'Current Salary': 79000, 'Leave Entitlement': 26},
    'E01033': {'Name': 'Asif Ali Khan', 'Current Salary': 90100, 'Leave Entitlement': 38}
}

# RabbitMQ configuration
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_QUEUE = 'activity_logs'


def verify_employee(employee_id):
    # Check if the employee ID is in the employee data.
    return employee_id in employees


def rabbitmq(employee_id, cmd, opt, cl_add):
    # Send information to RabbitMQ for logging.
    try:
        # Establish connection to RabbitMQ server

        connect = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
        ch = connect.channel()
        ch.queue_declare(queue=RABBITMQ_QUEUE)

        # Prepare message for RabbitMQ

        msg = f"Employee ID: {employee_id}, Command: {cmd}, Options: {opt}, Client Address: {cl_add}"
        ch.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=msg)

        print(f"Message Sent to RabbitMQ: {msg}")

        # Close RabbitMQ connection
        connect.close()
    except Exception as e:
        print(f"Error occur while sending message to RabbitMQ: {e}")


def handle_command(cl_s, cmd, cl_add):
    # Process the received command and send a response.
    try:
        print(f"Command received: {cmd}")

        if cmd.startswith('VERIFY'):
            # Verify employee ID
            employee_id = cmd.split(',')[1]
            if verify_employee(employee_id):
                res = f'VERIFIED,{employees[employee_id]["Name"]}'
            else:
                res = 'NOT RECOGNIZED'
        elif cmd.startswith('CSALARY'):
            # Retrieve current salary information
            employee_id = cmd.split(',')[1]
            if employee_id in employees:
                salary = employees[employee_id]['Current Salary']
                res = f"{employees[employee_id]['Name']}'s Current basic salary is: {salary}"
            else:
                res = "Sorry! I don't recognise that employee id"
        elif cmd.startswith('TSALARY'):
            # Retrieve total salary and overtime
            employee_id, year = cmd.split(',')[1:]
            if employee_id in employees:
                salary = employees[employee_id]['Current Salary']
                over_time = 3089
                res = f"{employees[employee_id]['Name']}'s Total Salary for {year}: Basic pay is, {salary}; & Overtime is, {over_time}"
            else:
                res = "Sorry! I don't recognise that employee id"
        elif cmd.startswith('CENTITLE'):
            # Retrieve leave entitlement
            employee_id = cmd.split(',')[1]
            if employee_id in employees:
                ent = employees[employee_id]['Leave Entitlement']
                res = f"{employees[employee_id]['Name']}'s Current annual leave entitlement are: {ent} days"
            else:
                res = "Sorry! I don't recognise that employee id"
        elif cmd.startswith('YTAKEN'):
            # Retrieve leave taken
            employee_id, year = cmd.split(',')[1:]
            if employee_id in employees:
                leave = 31
                res = f"{employees[employee_id]['Name']}'s Leave taken in {year} are: {leave} days"
            else:
                res = "Sorry! I don't recognise that employee id"
        elif cmd.startswith('CONTINUE'):
            res = "Continue command received!"
        else:
            res = "Invalid command!"

        print(f"Sending a response: {res}")

        # Send the information to RabbitMQ for logging
        rabbitmq(employee_id, cmd, None, cl_add)

    except Exception as e:
        print(f"Error processing command: {e}")
        res = f"Error processing command: {e}"

    cl_s.send(res.encode())


def handle_client(cl_s, dis_sys):
    # Handle communication with a client.
    print("Connected to:", dis_sys)

    while True:
        cmd = cl_s.recv(1024).decode()

        if cmd == 'EXIT':
            break

        # Process the received command
        handle_command(cl_s, cmd, dis_sys)

    cl_s.close()
    print("Client disconnected!")


def main():
    # Main server function.
    host = 'localhost'
    port = 8888

    # Set up server socket
    srv_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_s.bind((host, port))
    srv_s.listen()

    print("Server Launched")

    while True:
        # Accept incoming client connections
        cl_s, dis_sys = srv_s.accept()

        # Create a new thread to handle the client
        cl_thd = threading.Thread(target=handle_client, args=(cl_s, dis_sys))
        cl_thd.start()


if __name__ == "__main__":
    main()
