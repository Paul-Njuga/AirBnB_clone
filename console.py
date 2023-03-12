#!/usr/bin/python3
"""Entry point of the command interpreter."""
import cmd
import re
from models import storage


class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""
    prompt = '(hbnb) '

    def emptyline(self):
        return

    def do_EOF(self, line):
        """Quit command to exit the program\n"""
        return True

    def do_quit(self, line):
        """Quit command to exit the program\n"""
        return True

    def do_create(self, line):
        """Creates a new instance of BaseModel,
        & saves it to the JSON file."""
        if line == "" or line is None:
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            c = storage.classes()[line]()
            c.save()
            print(c.id)

    def do_show(self, line):
        """Prints the string representation of an instance,
        based on the class name and id."""
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                k = "{}.{}".format(words[0], words[1])
                if k not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[k])

    def do_destroy(self, line):
        """Deletes an instance based on class name & id,
        & saves changes into the JSON file."""
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                k = "{}.{}".format(words[0], words[1])
                if k not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[k]
                    storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances,
        based or not on the class name."""
        if line != "" or line is not None:
            if line not in storage.classes():
                print("** class doesn't exist **")
            else:
                lst = [str(obj) for key, obj in storage.all().items(
                ) if type(obj).__name__ == line]
                print(lst)
        else:
            lst = [str(obj) for key, obj in storage.all().items()]
            print(lst)

    def do_update(self, line):
        """Updates an instance based on the class name & id,
        by adding or updating attribute."""
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            all_objs = storage.all()
            cls_objs = {key: val for key, val in all_objs.items()}
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                k = "{}.{}".format(words[0], words[1])
                if k not in all_objs:
                    print("** no instance found **")
                elif len(words) < 3:
                    print("** attribute name missing **")
                elif len(words) < 4:
                    print("** value missing **")
                else:
                    attr_val = words[3]
                    """Check for string against regex"""
                    if re.search('^".*"$', attr_val):
                        """Remove double quotes"""
                        attr_val = attr_val.replace('"', '')
                    else:
                        """Handle non string (int || float)"""
                        if '.' in attr_val:
                            float(attr_val)
                        else:
                            int(attr_val)
                    if words[2] in [key for key, val in cls_objs.items()]:
                        """If key exists, update value."""
                        attr_name = words[2]
                        cls_objs[attr_name] = words[3]
                    else:
                        setattr(all_objs[k], words[2], attr_val)
                    all_objs[k].save()

    def do_count(self, args):
        """
        retrieves the number of instances of a class
        """
        count = 0
        for obj in storage.all().values():
            if obj.__class__.__name__ == args:
                count += 1
        print(count)

    def default(self, line):
        """Method to take care of following commands:
        <class name>.all()
        <class name>.count()
        <class name>.show(<id>)
        <class name>.destroy(<id>)
        <class name>.update(<id>, <attribute name>, <attribute value>)
        <class name>.update(<id>, <dictionary representation)
        Description:
            Creates a list representations of functional models
            Then use the functional methods to implement user
            commands, by validating all the input commands
        """
        names = ["BaseModel", "User", "State", "City", "Amenity",
                 "Place", "Review"]

        commands = {"all": self.do_all,
                    "count": self.do_count,
                    "show": self.do_show,
                    "destroy": self.do_destroy,
                    "update": self.do_update}

        args = re.match(r"^(\w+)\.(\w+)\((.*)\)", line)
        if args:
            args = args.groups()
        if not args or len(args) < 2 or args[0] not in names \
                or args[1] not in commands.keys():
            super().default(line)
            return

        if args[1] in ["all", "count"]:
            commands[args[1]](args[0])
        elif args[1] in ["show", "destroy"]:
            commands[args[1]](args[0] + ' ' + args[2])
        elif args[1] == "update":
            params = re.match(r"\"(.+?)\", (.+)", args[2])
            if params.groups()[1][0] == '{':
                dic_p = eval(params.groups()[1])
                for k, v in dic_p.items():
                    commands[args[1]](args[0] + " " + params.groups()[0] +
                                      " " + k + " " + str(v))
            else:
                rest = params.groups()[1].split(", ")
                commands[args[1]](args[0] + " " + params.groups()[0] + " " +
                                  rest[0] + " " + rest[1])

    def my_errors(self, line, args_number):
        """
        Displays error messages to user
        Args:
            line(any): gets user input using command line
            num_of_args(int): number of input arguments
        Description:
            Displays output to the use based on
            the input commands.
        """
        classes = [
        "BaseModel",
        "User",
        ]

        message = [
                    "** class name missing **",
                    "** class doesn't exist **",
                    "** instance id missing **",
                    "** no instance found **",
                    "** attribute name missing **",
                    "** value missing **"
        ]

        if not line:
            print(message[0])
            return 1
        args = line.split()
        if args_number >= 1 and args[0] not in classes:
            print(message[1])
            return 1
        elif args_number == 1:
            return 0
        if args_number >= 2 and len(args) < 2:
            print(message[2])
            return 1
        d = storage.all()

        for i in range(len(args)):
            if args[i][0] == '"':
                args[i] = args[i].replace('"', "")
        key = args[0] + '.' + args[1]
        if args_number >= 2 and key not in d:
            print(message[3])
            return 1
        elif args_number == 2:
            return 0
        if args_number >= 4 and len(args) < 3:
            print(message[4])
            return 1
        if args_number >= 4 and len(args) < 4:
            print(message[5])
            return 1
        return 0

    def do_destroy(self, args):
        """
        Deletes an instance based on the class name and id 
        Arguments:
            args: to enter with command: <class name> <id>
            Example: 'destroy BaseModel 121212'
        """

        if (self.my_errors(args, 2) == 1):
            return
        arguments = args.split()
        stores = storage.all()
        if arguments[1][0] == '"':
            arguments[1] = arguments[1].replace('"',"")
        key = arguments[0] + '.' + arguments[1]
        del stores[key]
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
