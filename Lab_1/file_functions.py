import pickle
class File_function:
    @staticmethod
    def load_faculties():
        with open('./db/faculties.db', 'rb') as f:
            faculties = pickle.load(f)
        return faculties

    @staticmethod
    def load_groups():
        with open('./db/groups.db', 'rb') as g:
            groups = pickle.load(g)
        return groups

    @staticmethod
    def load_students():
        with open('./db/students.db', 'rd') as s:
            students = pickle.load(s)
        return students

    @staticmethod
    def save_faculties(faculties):
        with open('./db/faculties.db', 'wb') as f:
            pickle.dump(faculties, f)

    @staticmethod
    def save_groups(groups):
        with open('./db/groups.db', 'wb') as g:
            pickle.dump(groups, g)

    @staticmethod
    def save_students(students):
        with open('./db/students.db', 'wb') as s:
            pickle.dump(students, s)