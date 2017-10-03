from file_functions import File_function

class Faculty(object):
    def __init__(self, fid, fname, groups):
        self.fid = fid
        self.fname = fname
        self.groups = groups


    def add_group(self, group):
        if group.gid not in self.groups:
            self.groups.append(group.gid)

    def remove_group(self, group):
        if group.gid in self.groups:
            self.groups.remove(group.gid)

    def __str__(self):
        res = "Faculty %s\n\tGroups:\n\t\t" % self.gid
        groupsList = File_function.load_groups()
        for g in self.groups:
            group = [item for item in groupsList.group if str(item.id) == str(g)]
            if group:
                res += group[0].__str__() + "\n\t\t"

        return res

class Faculties:
    def __init__(self):
        self.faculties = list()

    def add(self, gids):
        allGroups = File_function.load_groups()
        groups = []
        for gid in gids:
            group = [item for item in allGroups.groups if str(item.id) == str(gid)]
            if group:
                groups.append(gid)
        for i in range(1,self.faculties.__len__() + 2):
            if not any(str(item.id) == str(i) for item in self.faculties):
                name = input("")
                faculty = Faculty(str(i),name,groups)
                self.faculties.append(faculty)
                return faculty

    def delete(self,gid):
        faculty = self.get_faculty_by_id(gid)
        if faculty is not None:
            self.faculties.remove(faculty)
            return faculty
        else :
            return None

    def faculty_with_max_num_of_group(self):
        res = ""
        allFaculties = File_function.load_faculties()
        for faculty in self.faculties:
            max_len = max([len(i) for i in faculty.groups])
            targets = [item for item in allFaculties.faculties if max_len]

    def add_group_to_fac(self, faculty, group):
        faculty.add_group(group)

    def remove_group_from_fac(self, faculty, group):
        faculty.remove_group(group)
        if faculty.groups.__len__() == 0:
            return None
        else:
            return faculty

    def get_faculty_by_id(self, fid):
        faculty = [faculty for faculty in self.faculties if str(faculty.id) == str(fid)]
        if faculty :
            return faculty[0]
        else:
            return None

    def __str__(self):
        res = ""
        if self.faculties:
            for faculty in self.faculties:
                res += faculty.__str__()+ '\n'
        else:
            res = "No faculties in database"
        return res