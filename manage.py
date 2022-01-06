#!/usr/bin/env python
from payslip.payslip import command_help, migrate_db, destroy, generate_payslip


if __name__ == "__main__":
    command_help()
    while True:
        print("Type 'Exit' to stop run")
        command = input("\nType your command: ")
        if command.lower() == 'exit':
            break
        elif command.lower() == 'help':
            command_help()
        elif command.lower() == 'migrate':
            migrate_db()
        elif command.lower() == 'destroy':
            destroy()
        elif command.split()[0].lower() == 'generatemonthlypayslip':
            generate_payslip(command)
        else:
            print("Your command is invalid, type 'help' to see valid commands")