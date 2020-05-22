import web
import smbus

import old_imu as imu
from i2cutils import i2c_raspberry_pi_bus_number

urls = (
    '/', 'index'
)

bus = smbus.SMBus(i2c_raspberry_pi_bus_number())
imu_controller = imu.IMU(bus, 0x68, 0x5c, "IMU")
imu_controller.set_compass_offsets(9, -10, -140)  # значения, полученные на этапе калибровки
app = web.application(urls, globals())


class index:
    def GET(self):
        (pitch, roll, yaw) = imu_controller.read_pitch_roll_yaw()
        result = "%.2f %.2f %.2f" % (pitch, roll, yaw)
        return result


if __name__ == "__main__":
    app.run()
