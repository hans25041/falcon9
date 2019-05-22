"""
Falcon9 provides a Python class for interfacing with the Falcon9 rocket.

The class models the spacecraft and provides an interface for controlling the
rocket.
"""

from abc import ABC
from time import sleep
from sys import exit
import inflect


class Flight:
    """A class to model the flight of a rocket"""

    def __init__(self, rocket):
        """Attach the rocket that will fly"""
        self.rocket = rocket

    def __str__(self):
        """Return the friendly representation of the flight."""
        return "Flight of {} Rocket".format(type(rocket).__name__)

    def countDown(self, delay):
        print("Launch in t-minus")
        for i in range(delay,0,-1):
            print(i)
            sleep(1)
        print("Blast off! 🚀")

    def launch(self):
        try:
            self.rocket.launch()
        except CatastrophicFailure:
            print("🚀 💥 CatastrophicFailure during launch")
            exit(1)

    def detatchFirstStage(self):
        """Detatch the first stage of the rocket and return it for recovery."""
        try:
            return self.rocket.detatchFirstStage() 
        except CatastrophicFailure:
            print("🚀 💥 CatastrophicFailure detatching first stage")
            exit(1)

    def jetisonPayload(self):
        self.rocket.jetisonPayload()

    def recoverStage(self, stage):
        try:
            stage.recover()
        except AttributeError:
            print("{} cannot be recovered.".format(str(stage)))
        except CatastrophicFailure:
            print("🚀 💥 CatastrophicFailure recovering first stage")
            exit(1)


class Falcon9:
    """Falcon 9 is a 2-stage rocket."""

    def __init__(self):
        """Build the rocket"""
        self.firstStage = FirstStage()
        self.secondStage = SecondStage()
        self.interstage = InterStage(self.firstStage, self.secondStage)
        self.payload = DragonSpacecraft()

    def __str__(self):
        """A string representation of the rocket"""
        return ("Falcon9 Rocket\n"
                "\t" + str(self.firstStage) + "\n"
                "\t" + str(self.interstage) + "\n"
                "\t" + str(self.secondStage) + "\n"
                "\t" + str(self.payload)
               )

    def launch(self):
        """Launch the rocket."""
        self.firstStage.launch()

    def detatchFirstStage(self):
        """Detatch and return the first stage."""
        firstStage = self.firstStage
        self.interstage.detatchFirstStage()
        self.firstStage = None
        self.jetisonInterstage()
        self.secondStage.burn(0.50)
        return firstStage # return the stage so it can be recovered.

    def jetisonInterstage(self):
        """Jetison the interstage to allow the second stage burn."""
        self.interstage = None

    def jetisonPayload(self):
        """Detatch the second stage from the payload."""
        self.secondStage = None


class Engine(ABC):
    """Baseclass for engines
    
    Constants:
        FUEL_TYPE: A tuple of the fuel blend used by the rocket.
        POWER_CYCLE_TYPE: The name of the power cycle type.
        VACUUM_THRUST: Maximum thrust in a vacuum. (kN)
        SEA_LEVEL_THRUST: Maximum thrust at sea level. (kN)
        THRUST_TO_WEIGHT: The ratio of thrust to weight.
        CHAMBER_PRESSURE: The pressure in the chamber. (MPa)
        DIAMETER: The diameter of the engine. (M)
        DRY_WEIGHT: The weight (mass) of the empty engine. (kg)
        BURN_RATE: How many seconds it takes to burn 1% fuel at full throttle.
    """

    BURN_RATE = None

    def __str__(self):
        """The class name is the string representation"""
        return type(self).__name__

    def burn(self, throttle=0.0, duration=1):
        """
        Burn the engine

        :param float throttle: percentage of max throttle expressed as float.
        :param int duration: duration of burn in seconds.
        """
        if throttle > 1.0 or throttle < 0.0:
            raise ValueError("throttle must have a value between 0.0 and 1.0")

        fuelBurn = self.BURN_RATE * throttle * duration
        if fuelBurn < self.fuelLevel:
            self.fuelLevel -= fuelBurn
        else:
            self.fuelLevel = 0.0
            raise BurnOutException()


class Merlin(Engine):
    """
    Merlin engine class

    The engine burns 0.5% of its fuel capacity every second that it is at full
    throttle.
    """

    BURN_RATE = 0.005

    def __init__(self, fuelLevel=1.0):
        """Initialize the Merlin rocket with a full fuel tank and no throttle"""
        self.fuelLevel = fuelLevel

    def __repr__(self):
        return "Engine(fuelLevel={},throttle={})".format(self.fuelLevel)


class Stage(ABC):
    """Baseclass for rocket stages"""

    BURN_TIME = None

    def __str__(self):
        s = type(self).__name__ # The stage name
        ec = len(self.engines) # Number of engines
        et = type(self.engines[0]).__name__ # The class of the engine objects
        p = inflect.engine().plural("engine", ec) # Pluralize `engine`
        return "{}: consisting of {} {} {}".format(s, ec, et, p)


class FirstStage(Stage):
    """
    The First Stage component of the Falcon9 spacecraft
    
    This stage contains 9 Merlin engines arranged with one in the center with
    the other eight forming an octogon around the center.

    The 0th engine is in the center. The other 8 engines make up the
    vertices of a regular octagon. Each engine with index > 0 is exactly
    opposite that index + 4. The x axis connects 1 and 5. The Y axis
    connects 3 and 7.
    """

    BURN_TIME = 162
    DIRECTIONS = {"up", "down", "left", "right" }
    OPPOSITE_DIR = {
        "up": "down",
        "down": "up",
        "right": "left",
        "left": "right"
    }

    def __init__(self):
        """
        Build the first stage with 9 Merlin engines.
        """
        self.engines = [Merlin() for i in range(9)]


    def __repr__(self):
        return "FirstStage()"

    def launch(self):
        self.burn(0.85, self.BURN_TIME)

    def tilt(self, direction, baseThrottle=0.7):
        """
        Tilt in the direction specified.

        :param string direction: up, down, left, right, or straight
        :param float baseThrottle: minimum engine throttle.
        """
        if direction not in self.DIRECTIONS:
            ds = ", ".join(directions)
            raise ValueError("Direction must be one of {}".format(ds))

        # Directional engines burn at 25% higher throttle than base.
        elevatedThrottle = baseThrottle * 1.25
        # No engine can run at more than 100% throttle.
        highThrottle = elevatedThrottle if elevatedThrottle < 1.0 else 1.0

        # Select the engines to fire when moving in the specified direction.
        if direction == "up":
            engines = {2, 3, 4}
        elif direction == "right":
            engines = {4, 5, 6}
        elif direction == "down":
            engines = {6, 7, 8}
        else:
            engines = {1, 2, 8}

        for i, e in enumerate(self.engines):
            if i in engines:
                try:
                    e.burn(highThrottle, 1)
                except BurnOutException:
                    print("Engine {} burned out.".format(i))
            else:
                try:
                    e.burn(baseThrottle, 1)
                except BurnOutException:
                    print("Engine {} burned out.".format(i))
        self._testCatistrophicFailure()

    def burn(self, throttle=0.7, duration=0):
        for i, e in enumerate(self.engines):
            try:
                e.burn(throttle, duration)
            except BurnOutException:
                print("Engine {} burned out.".format(i))
        self._testCatistrophicFailure()

    def strafe(self, direction, duration):
        self.tilt(direction)
        self.burn(0.7, duration)
        # tilt back to straight
        self.tilt(self.OPPOSITE_DIR[direction])

    def recover(self):
        self.strafe("right", 10)
        self.strafe("up", 5)
        self.burn(0.5, 5)
        self.burn(0.3, 5)
        self.burn(0.1, 5)
        self.burn(0, 1)

    def _testCatistrophicFailure(self):
        # The first stage can tolerate 2 burned out engines.
        burnedOutEngines = [e for e in self.engines if e.fuelLevel == 0.0]
        if len(burnedOutEngines) > 2:
            raise CatastrophicFailure()


class SecondStage(Stage):
    """The Second Stage component of the Falcon9 spacecraft"""

    BURN_TIME = 397

    def __init__(self):
        """The second stage contains a single Merlin engine."""
        self.engines = [Merlin()]

    def burn(self, throttle):
        for e in self.engines:
            try:
                e.burn(throttle, self.BURN_TIME)
            except BurnOutException:
                # There is only one engine. If it burns out, game over.
                raise CatastrophicFailure()


class InterStage:
    """
    The interstage component of the Falcon9 spacecraft

    The interstage is not a true stage, it is the composite structure that
    connects the first and second stages and houses the release and separation
    system.
    """

    def __init__(self, firstStage, secondStage):
        self.firstStage = firstStage
        self.secondStage = secondStage

    def __str__(self):
        return "InterStage: composite structure connecting stages 1 and 2"

    def detatchFirstStage(self):
        self.firstStage = None


class Payload(ABC):
    """
    Baseclass for all payloads

    Constants:
        HEIGHT: The height in meters
        DIAMETER: The diameter in meters
    """

    def __str__(self):
        return "Payload: " + type(self).__name__

    HEIGHT = None
    DIAMETER = None


class DragonSpacecraft(Payload):
    """The Dragon cargo or crew capsule"""

    HEIGHT = 8.1
    DIAMETER = 3.7


class CompositeFairing(Payload):
    """Payload fairing for delivering satelites into LEO, GTO, and beyond."""

    HEIGHT = 13.1
    DIAMETER = 5.2


class BurnOutException(Exception):
    pass


class CatastrophicFailure(Exception):
    pass


if __name__ == "__main__":
    f9 = Falcon9()
    flight = Flight(f9)
    flight.countDown(3)
    flight.launch()
    firstStage = flight.detatchFirstStage()
    print("First stage detatched")
    flight.recoverStage(firstStage)
    print("First stage recovered")
    flight.jetisonPayload()
    print("Payload jetisoned")
