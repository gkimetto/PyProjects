from wait_for import wait_for
import time


class Incrementor:
    value = 0

    def i_sleep_a_lot(self):
        time.sleep(10)
        self.value +=1
        return self.value

incman = Incrementor()

ec, tc = wait_for(incman.i_sleep_a_lot, fail_condition = 0, delay =.05)
print ("Function output {} in time {} ".format(ec, tc))
