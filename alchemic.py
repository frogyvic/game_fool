from enum import Enum
class Element(Enum):
    fire=("Fire", (205, 92, 92))
    water=("Water",(70, 130, 180)  )
    earth=("Earth",(0, 100, 0)  )
    wind=("Wind"  ,(245, 245, 220)  )
    lava=("Lava",(139, 0, 0))
    dirt=("Dirt",(139, 69, 19))
    hurricane=("Hurricane",(105, 105, 105))
    stream=("Stream",(255, 228, 225))

child_elements = [
    [Element.fire, Element.earth, Element.lava],
    [Element.earth, Element.water, Element.dirt],
    [Element.wind, Element.wind, Element.hurricane],
    [Element.fire, Element.water, Element.stream]
]

class Game:
    def __init__(self):
        self.elements =[Element.fire,Element.water,Element.earth,Element.wind]

    def print_elements(self):
        print("Все ваши элементы:")
        for element in self.elements:
            print(f"\033[38;2;{element.value[1][0]};{element.value[1][1]};{element.value[1][2]}m{element.value[0]}\033[0m")
    def mix_elements(self,first_element:Element,second_element:Element):
        find=False
        # print(first_element,second_element)
        for i in child_elements:
            # print(i[0],i[1])
            # print(second_element,first_element)
            if {first_element,second_element} == {i[0],i[1]}:
                # print(i[2])
                if i[2] in child_elements:
                    print("вы уже открыли этот элемент")
                else:
                    print("")
                    self.elements.append(i[2])
                    print(f"открыт новый элемент:\033[38;2;{i[2].value[1][0]};{i[2].value[1][1]};{i[2].value[1][2]}m{i[2].value[0]}\033[0m")
                find = True
        if not find:
            print("Такого элемента нет, попробуйте другую комбинацию")


                           

g=Game()
# print(len(g.elements))
# print(len(child_elements))
while len(g.elements)<(len(child_elements)+4):
    g.print_elements()
    firstEl = -1
    while (len(g.elements)-1)<firstEl or firstEl<0:
        try:
            firstEl=int(input(f"выберите первый элемент для смешения(0-{len(g.elements)-1}):"))
        except:
            print(f"Введите число от 0 до {len(g.elements)-1}")
    secondEl = -1
    while (len(g.elements) - 1) < secondEl or secondEl < 0:
        try:
            secondEl = int(input(f"выберите второй элемент для смешения(0-{len(g.elements) - 1}):"))
        except:
            print(f"Введите число от 0 до {len(g.elements) - 1}")
    g.mix_elements(g.elements[firstEl],g.elements[secondEl])