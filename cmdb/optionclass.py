# coding:utf-8
__author__ = 'ZengKing'


class SonMods():
    def __init__(self, name, cname, url):
        self.name = name
        self.url = url
        self.cname = cname


class FatherMods():
    def __init__(self, name, son_mod):
        self.son_mods = []
        self.name = name
        self.son_mods.append(son_mod)


    def add_son_mod(self, son_mod):
        self.son_mods.append(son_mod)

    def get_son_mods(self):
        return self.son_mods


class GrandFatherMods():
    def __init__(self, name):
        self.father_mods = []
        self.name = name

    def add_father_mod(self, f_mod):
        f = 0
        for fa_mod in self.father_mods:
            if fa_mod.name == f_mod.name:
                fa_mod.son_mods.extend(f_mod.get_son_mods())
                f=1
        if f==0:
            self.father_mods.append(f_mod)





