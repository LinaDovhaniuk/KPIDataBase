from file_functions import File_function

class Group(object):

    def __init__(self, gid, gname, students):
        self.gid = gid
        self.gname = gname
        self.students = students

    def __str__(self):
        return "Group: id = %s, name = %s, number of students = %.2f" % (self.gid, self.gname, self.students)


class Groups(object):
    def __init__(self, groups):
        self.groups = groups

    def add(self, gname, students):
        for i in range(1, self.groups.__len__() + 2):
            if not any(str(item.gid) == str(i) for item in self.groups):
                group = Group(str(i), gname,students)
                self.groups.append(group)
                return group

    def update(self, gid, newName, newNumofStud):
        group = self.get_group_by_id(gid)
        if group is not None:
            group.gname = newName
            group.students = newNumofStud
        return group

    def get_group_by_id(self, gid):
        group = [item for item in self.groups if str(item.gid) == str(gid)]
        if group :
            return group[0]
        else :
            return None

    def remove(self, gid):
        del_group = [item for item in self.groups if str(item.gid) == str(gid)]
        if del_group:
            self.groups.remove(del_group[0])
            return del_group[0]
        else :
            return None

    def __str__(self):
        res = ""
        if self.groups:
            for group in self.groups:
                #res.join(group.__str__() + "\n")
                res += str(group)
        else:
            res = "No groups in database"
        return res

    