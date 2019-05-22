import unittest
import models

class TestFalcon9Model(unittest.TestCase):

    def testFalcon9Initialization(self):
        f9 = models.Falcon9()
        self.assertIsInstance(f9, models.Falcon9)

    def testFalcon9StringRepresentation(self):
        f9 = models.Falcon9()
        s = ("Falcon9 Rocket\n"
         "\tFirstStage: consisting of 9 Merlin engines\n"
         "\tInterStage: composite structure connecting stages 1 and 2\n"
         "\tSecondStage: consisting of 1 Merlin engine\n"
         "\tPayload: DragonSpacecraft"
        )
        self.assertEqual(str(f9), s)

    def testFlightInitialization(self):
        f9 = models.Falcon9()
        flight = models.Flight(f9)
        self.assertIsInstance(flight, models.Flight)

    def testMerlinInitialization(self):
        m1 = models.Merlin()
        self.assertIsInstance(m1, models.Merlin)
        self.assertEqual(m1.fuelLevel, 1.0)

        m2 = models.Merlin(0.5)
        self.assertIsInstance(m1, models.Merlin)
        self.assertEqual(m2.fuelLevel, 0.5)

    def testFirstStageInitialization(self):
        fs = models.FirstStage()
        self.assertIsInstance(fs, models.FirstStage)
        self.assertEqual(len(fs.engines), 9)

    def testSecondStageInitialization(self):
        ss = models.SecondStage()
        self.assertIsInstance(ss, models.SecondStage)
        self.assertEqual(len(ss.engines), 1)

    def testInterStageInitialization(self):
        fs = models.FirstStage()
        ss = models.SecondStage()
        istage = models.InterStage(fs, ss)
        self.assertIsInstance(istage, models.InterStage)

    def testDragonSpacecraftInitialization(self):
        ds = models.DragonSpacecraft()
        self.assertIsInstance(ds, models.DragonSpacecraft)

    def testCompositeFairingInitialization(self):
        ds = models.CompositeFairing()
        self.assertIsInstance(ds, models.CompositeFairing)

    def testInterStageDetatchFirstStage(self):
        fs = models.FirstStage()
        ss = models.SecondStage()
        istage = models.InterStage(fs, ss)
        self.assertIsInstance(istage.firstStage, models.FirstStage)
        istage.detatchFirstStage()
        self.assertIsNone(istage.firstStage)

    def testSecondStageBurn(self):
        ss = models.SecondStage()
        self.assertEqual(ss.engines[0].fuelLevel, 1.0)
        ss.burn(0.50)
        self.assertLess(ss.engines[0].fuelLevel, 0.01)

    def testFirstStageLaunch(self):
        fs = models.FirstStage()
        [self.assertEqual(e.fuelLevel, 1.0) for e in fs.engines]
        fs.launch()
        [self.assertLess(e.fuelLevel, 0.4) for e in fs.engines]

    def testFirstStageCatastrophicFailure(self):
        fs = models.FirstStage()
        with self.assertRaises(models.CatastrophicFailure) as context:
            fs.burn(1.0, 200)

    # Omitting other FirstStage tests

    def testMerlinBurn(self):
        m = models.Merlin()
        self.assertEqual(m.fuelLevel, 1.0)
        m.burn(1.0, 10)
        self.assertAlmostEqual(m.fuelLevel, 0.95)
        m.burn(0.5, 20)
        self.assertAlmostEqual(m.fuelLevel, 0.90)

    def testFalcon9DetatchFirstStage(self):
        f9 = models.Falcon9()
        self.assertIsInstance(f9.firstStage, models.FirstStage)
        self.assertIsInstance(f9.secondStage, models.SecondStage)
        self.assertIsInstance(f9.interstage, models.InterStage)
        self.assertIsInstance(f9.payload, models.DragonSpacecraft)

        f9.detatchFirstStage()
        self.assertIsNone(f9.firstStage)
        self.assertIsNone(f9.interstage)

    # Omitting other Falcon9 tests

    def testFlight(self):
        try:
            f9 = models.Falcon9()
            flight = models.Flight(f9)
            flight.countDown(0)
            flight.launch()
            firstStage = flight.detatchFirstStage()
            flight.recoverStage(firstStage)
            flight.jetisonPayload()
        except models.CatastrophicFailure:
            self.fail("Flight test raised a CatastrophicFailure")


if __name__ == "__main__":
    unittest.main()
