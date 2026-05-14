'''
Liskov Substitution Principle (LSP)

Concept - 
It states that objects of derived classes should be able to substitute objects of base class.
It must not break the contract of the base class.
The issue it resolves is that if the base class object is replaced with a derived class object, the program should not break.

Interview Explanation - 
"LSP says that anywhere you use a base class, you should be able to swap in any of its subclasses without breaking the program."

The bad example: BirdBad promises three things — make_sound(), fly(), and swim(). 
If I write a function that takes any BirdBad and calls bird.fly(), it works fine for SparrowBad, 
but explodes with PenguinBad because it raises NotImplementedError. I can't freely substitute one subclass for another — 
LSP is violated.

The root cause is that BirdBad has a too-broad contract. Not all birds fly. Not all birds swim. 
By putting both in one class, we force subclasses to either implement something they can't do, or break the contract.

The fix: I split the hierarchy. Bird only promises make_sound() — something all birds genuinely do. 
FlyingBird adds fly(), SwimmingBird adds swim(). Now Penguin extends SwimmingBird — it's never asked to fly. 
Sparrow extends FlyingBird — it's never asked to swim. Duck extends both because it can do both.

Now if I write a function that takes a FlyingBird, I can pass in a Duck or a Sparrow and fly() always works. 
If I write a function that takes a SwimmingBird, I can pass in a Duck or a Penguin and swim() always works. 
Every subclass fully honors its parent's contract — LSP is satisfied.
'''

from abc import ABC, abstractmethod

class BirdBad:
    def make_sound(self) -> str:
        pass
    def fly(self) -> str:
        pass
    def swim(self) -> str:
        pass

class PenguinBad(BirdBad):
    def fly(self) -> str:
        raise NotImplementedError("Penguins cannot fly")
    def swim(self) -> str:
        return "Penguins can swim"
    

class SparrowBad(BirdBad):
    def fly(self) -> str:
        return "Sparrows can fly"
    def swim(self) -> str:
        raise NotImplementedError("Sparrows cannot swim")


class Bird(ABC):
    @abstractmethod
    def make_sound(self) -> str:
        pass

class FlyingBird(Bird):
    @abstractmethod
    def fly(self) -> str:
        pass

class SwimmingBird(Bird):
    @abstractmethod
    def swim(self) -> str:
        pass

class Penguin(SwimmingBird):
    def make_sound(self) -> str:
        return "Penguins make sound"

    def swim(self) -> str:
        return "Penguins can swim"

class Duck(FlyingBird, SwimmingBird):
    def make_sound(self) -> str:
        return "Ducks make sound"
    def fly(self) -> str:
        return "Ducks can fly"
    def swim(self) -> str:
        return "Ducks can swim"

class Sparrow(FlyingBird):
    def make_sound(self) -> str:
        return "Sparrows make sound"
    def fly(self) -> str:
        return "Sparrows can fly"

if __name__ == "__main__":
    penguin = Penguin()
    duck = Duck()
    sparrow = Sparrow()
    print(penguin.make_sound())
    print(duck.make_sound())
    print(sparrow.make_sound())
    print(duck.fly())
    print(sparrow.fly())
    print(penguin.swim())
    print(duck.swim())