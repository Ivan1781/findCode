
class Finder:
    position_of_element = 0

    # функция прохода по всем элементам списка, в котором могут быть вложенные массивы
    #
    def find_in_list(self, lis):
        for elem in lis:
            if not elem:
                print("Пусто")
            elif type(elem) == list:
                print('---вызываенм заново---')
                self.find_in_list(elem)
            else:
                print(elem)

#
# liis = [['spis', ['d', ['yyy']]], 'abc']
# # for a in liis:
# #     print(type(a))
# #
# fender = Finder()
# fender.find_in_list(liis)
