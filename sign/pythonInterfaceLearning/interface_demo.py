from zope.interface.declarations import implementer
from zope.interface import Interface


class IHost(Interface):
    def sayGoodMorning(self, host):
        '''say good morning'''


@implementer(IHost)
class Host:
    def sayGoodMorning(self, guest):
        return "say goodmorning to %s" % guest




class Host_son(Host):
    def sayGoodMorning(self, father1):
        return "Hello, %s" % father1


if __name__ == '__main__':
    father = Host()
    son = Host_son()
    father_to_son = father.sayGoodMorning('tom')
    son_to_father = son.sayGoodMorning('gary')
    print(father_to_son)
    print(son_to_father)

