from file_functions import File_function
from faculty import Faculties
from group import Groups


class Functions:
    def start(self):
        fileFunc = File_function()

        faculties = fileFunc.load_faculties()
        groups = fileFunc.load_groups()
        menu = self.show()

        while True:
            choice = input('\n' + menu + "\n\n>>>\t")

            if choice == '1':
                self.show_groups(groups)

            elif choice == '2':
                self.create_group(groups)

            elif choice == '3':
                self.update_group(groups)

            elif choice == '4':
                self.remove_group(groups)

            elif choice == '5':
                self.show_faculties(faculties)

            elif choice == '6':
                self.create_faculty(faculties)

            elif choice == '7':
                self.add_group_to_fac(faculties, groups)

            elif choice == '8':
                self.remove_group_from_fac(faculties, groups)

            elif choice == '9':
                self.remove_faculty(faculties)

            elif choice == '10':
                self.show_max_num_of_group(faculties)

            elif choice == 'e':
                break

            fileFunc.save_faculties(faculties)
            fileFunc.save_groups(groups)

    def show_groups(self, groups):
        self.print_not_none(groups)

    def create_group(self, groups):
        try:
            name = input("\n Group : ")
            numOfStud = float(input("Students : "))

            group = groups.add(name, numOfStud)
            print(group)
        except ValueError:
            print("Wrong data")

    def update_group(self, groups):
        gid = input("\nWhich group do you want to change?\n>>> ")
        group = groups.get_group_by_id(gid)
        self.print_not_none(group)
        if group is not None:
            try:
                newName = input("New name(Old: %s) = " % group.gname)
                newNumOfStud = float(input("New number of students(Old: %f) = " % group.students))

                group = groups.update(gid, newName, newNumOfStud)

                self.print_not_none(group)
            except ValueError:
                print("Wrong data")

    def remove_group(self, groups):
        gid = input("\nWhich group do you want to delete?\n>>> ")
        group = groups.remove(gid)
        self.print_not_none(group)

    def show_faculties(self, faculties):
        self.print_not_none(faculties)

    def create_faculty(self, faculties):
        gids = str(input("\nWhich groups do you want to include to faculty?(id1;id2...)\n>>> "))
        listOfid = gids.split(sep=';')
        groupsList= []
        for g in listOfid:
            groupsList.append(g.replace('', ''))
        if groupsList:
            faculty = faculties.add(groupsList)
            self.print_not_none(faculty)
        else :
            print("Faculty without groups!")

    def add_group_to_fac(self,faculties, groups):
        facultyId = input("Which faculty do you want to update?(id): ")
        faculty = faculties.get_faculty_by_id(facultyId)
        if faculty is not None:
            groupId = input("Which group do you want to add?(id): ")
            group = groups.get_group_by_id(groupId)

            if group is not None:
                faculties.add_group_to_fac(faculty, group)
                self.print_not_none(faculty)
            else:
                print("No such group in database!")
        else:
            print("No such faculty in database")

    def remove_group_from_fac(self, faculties, groups):
        facultyId = input("Which faculty do you want to update?(id): ")
        faculty = faculties.get_faculty_by_id(facultyId)
        if faculty is not None:
            groupId = input("Which group do you want to remove?(id): ")
            group = groups.get_group_by_id(groupId)

            if group is not None:
                faculty = faculties.remove_group_from_fac(faculty, group)
                if faculty is not None:
                    print(faculty)
                else :
                    print("Faculty was deleted! ")
            else:
                    print("No such group in database!")
        else:
            print("No such faculty in database")

    def remove_faculty(self,faculties):
        fid = input("\nWhich faculty do you want to delete?\n >>> ")
        faculty = faculties.delete(fid)
        self.print_not_none(faculty)

    def show_max_num_of_group(self, faculties):
        print("Result : \n\t")
        print(faculties.faculty_with_max_num_of_group())

    def  print_not_none(self, obj):
        if obj is not None:
            print(obj)
        else:
            print("No such Object in database!")

    def show(self):
        with open('./db/menu.txt', 'r') as m:
            menu = m.read()
        return menu

