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
            cls_obj = {key: val for key, val in all_objs.items()}
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                k = "{}.{}".format(words[0], words[1])
                if k not in all_objs:
                    print("** no instance found **")
                elif words[2] == "" or words[2] is None:
                    print("** attribute name missing **")
                elif words[3] == "" or words[3] is None:
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
                    if words[2] in [key for key, val in cls_obj.items()]:
                        attr_name = words[2]
                        cls_obj[attr_name] = words[3]
                    else:
                        setattr(all_objs[k], words[2], attr_val)
                    all_objs[k].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
