class Driver:
    def __init__(self, ecu):
        self.ecu = ecu

    def press_accelerator(self):
        print("\n[Driver] 가속 페달 밟음")
        self.ecu.receive_accelerator_input()

    def press_brake(self):
        print("\n[Driver] 브레이크 밟음")
        self.ecu.receive_brake_input()


class ECU:
    def __init__(self, tcm):
        self.tcm = tcm
        self.speed = 40  # km/h

    def receive_accelerator_input(self):
        self.speed += 20  # 가속 시 속도 증가
        rpm = self.calculate_rpm()
        torque = 250
        print(f"[ECU] 가속: 속도 = {self.speed} km/h, RPM = {rpm}")
        self.tcm.process_acceleration(rpm, self.speed)

    def receive_brake_input(self):
        self.speed = max(0, self.speed - 15)  # 감속 시 속도 감소
        print(f"[ECU] 감속: 속도 = {self.speed} km/h")
        self.tcm.process_braking(self.speed)

    def calculate_rpm(self):
        # 단순한 RPM 계산 공식 (예시)
        return 800 + self.speed * 30

    def notify_driver(self, action):
        print(f"[ECU] 차량 {action} 반영 완료")


class TCM:
    def __init__(self, transmission, ecu):
        self.transmission = transmission
        self.ecu = ecu

    def process_acceleration(self, rpm, speed):
        print("[TCM] 가속 분석 중...")
        if rpm > 2500 and self.transmission.current_gear < 6:
            self.transmission.shift_up()
        self.ecu.notify_driver("가속")

    def process_braking(self, speed):
        print("[TCM] 감속 분석 중...")
        if speed < 50 and self.transmission.current_gear > 1:
            self.transmission.shift_down()
        self.ecu.notify_driver("감속")


class Transmission:
    def __init__(self):
        self.current_gear = 2

    def shift_up(self):
        self.current_gear += 1
        print(f"[Transmission] 기어 업 → 현재 기어: {self.current_gear}")

    def shift_down(self):
        self.current_gear -= 1
        print(f"[Transmission] 기어 다운 → 현재 기어: {self.current_gear}")


# ---------------------------
# 시뮬레이션 실행
# ---------------------------
if __name__ == "__main__":
    transmission = Transmission()
    ecu = ECU(None)
    tcm = TCM(transmission, ecu)
    ecu.tcm = tcm
    driver = Driver(ecu)

    print("=== 자동변속기 시뮬레이션 시작 ===")
    
    driver.press_accelerator()  # 1차 가속
    driver.press_accelerator()  # 2차 가속
    driver.press_brake()        # 감속

    print("\n=== 시뮬레이션 종료 ===")
