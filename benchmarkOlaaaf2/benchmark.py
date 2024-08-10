import multiprocessing
import itertools
import gc

import time

from ex_KiwiMilkshake import KiwiMilkshakeExample
from ex_KiwiMilkshakeNoBanana import KiwiMilkshakeNoBananaExample
from ex_KiwiMilkshakeSameNumberOfFruitTypes import KiwiMilkshakeSameNumberOfFruitTypesExample
from ex_CarrotCabbageSalad import CarrotCabageSaladExample
from ex_Pie import PieExample
from ex_BreastCancer import BreastCancerExample
from ex_BreastCancerNumerical import BreastCancerNumericalExample
from ex_HighDistance import HighDistanceExample
from ex_CombinedMilkshake import CombinedMilkshakeExample
from ex_CombinedSalad import CombinedSaladExample

def run(cls, a, b, c):

    print("--------------")
    print(cls.__name__)
    print(a[1], ";", b[1], ";", c[1])

    start = time.perf_counter()

    ex = cls()    
    ex.run(a[0], b[0], c[0])

    print(time.perf_counter() - start, "\n")

if __name__ == "__main__":

    exList = [KiwiMilkshakeExample, KiwiMilkshakeNoBananaExample, KiwiMilkshakeSameNumberOfFruitTypesExample,\
              CarrotCabageSaladExample, PieExample, BreastCancerExample, BreastCancerNumericalExample,\
              HighDistanceExample, CombinedMilkshakeExample, CombinedSaladExample]

    TIMEOUT = 300

    dkInclusion = {"conversion": True,
                "existence": True,
                "taxonomy": False,
                "miscellanous": True}
    
    for exClass in exList:

        for dkInclu, withTableaux, withMaxDist in itertools.product([({}, "Full DK"), (dkInclusion, "Partial DK (Without taxonomy)")],\
                                                                    [(False, "Without Tableaux"), (True, "With Tableaux")],\
                                                                    [(False, "Without Max Dist"), (True, "With Max Dist")]):
            
            
            gc.collect()

            thread = multiprocessing.Process(target=run, args=(exClass, dkInclu, withTableaux, withMaxDist))
            thread.start()
            thread.join(timeout=TIMEOUT)

            if thread.is_alive():
                thread.terminate()
                thread.join()
                
                print("--------------")
                print(exClass.__name__)
                print(dkInclu[1], ";", withTableaux[1], ";", withMaxDist[1])
                print("Timeout\n")
