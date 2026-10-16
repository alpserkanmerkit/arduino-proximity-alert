"""proximity-alert wiring diagrams (Tinkercad/Fritzing style), drawn with ../../tools/wiring_kit.py.

Run:  python draw_wiring.py   -> wiring-v1-v2.svg and wiring-final-fan.svg (+ .pins.json) next to this file
PNG:  python ../../tools/render_png.py   (renders every docs/*.svg in the repo with headless Edge/Chrome)

Pins (OLGU): v1-simple.ino, read from the original IDE screen in the N3 video:
  TRIG=D9, ECHO=D10, redLed=D3, yellowLed=D5 (a BLUE LED on the real board), greenLed=D6, motorPin=D11.
  v2: pins not visible in the video -> assumed identical (stated in v2-advanced.ino).
  Final fan build: original sketch not preserved -> same pins assumed (stated in final-fan.ino).
The fan driver (TIP120, 1N4007, 4xAA) is a RECOMMENDED circuit: the driver on the original breadboard
is not visible in any recording.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
from wiring_kit import Sheet, BY, ROW, cx, hole, pin_xy, rounded, R220, R1K  # noqa: E402

SENSOR = [42, 43, 44, 45]          # HC-SR04 VCC TRIG ECHO GND, row a
LANE = {"D6": BY + 200, "D5": BY + 210, "D3": BY + 220}   # lanes in the centre gap
BEND = {"D6": 510, "D5": 530, "D3": 550}
FAN_B = 50                          # TIP120 B=50, C=51, E=52 (row g)

SYM = {"D9": ["trigPin"], "D10": ["echoPin"], "D3": ["redLed", "redLedPin"],
       "D5": ["yellowLed", "yellowLedPin", "blueLed"], "D6": ["greenLed", "greenLedPin"], "D11": ["motorPin"]}


def power_and_sensor(s):
    p = pin_xy("5V")
    s.uno_wire("5v", 1, "5V", [(30, p[1]), (30, BY + 458), (cx(3) + 10, BY + 458), (cx(3) + 10, ROW["B+"]),
                               hole(3, "B+")], (30, BY + 300), "bottom + rail")
    p = pin_xy("GND")
    s.uno_wire("gnd", 2, "GND", [(44, p[1]), (44, BY + 440), (cx(1), BY + 440), hole(1, "B-")],
               (180, BY + 440), "bottom − rail")
    s.hcsr04(SENSOR)
    a = hole(SENSOR[0], "e")
    s.wire("5v", 3, [a, hole(SENSOR[0], "B+")], (a[0] - 16, BY + 290))
    a = hole(SENSOR[3], "e")
    s.wire("gnd", 4, [a, hole(SENSOR[3], "B-")], (a[0] + 16, BY + 290))
    s.between_rows("trig", 5, "D9", SENSOR[1], "e", (cx(36), pin_xy("D9")[1]), "HC-SR04 TRIG", SYM["D9"])
    s.between_rows("echo", 6, "D10", SENSOR[2], "d", (cx(30), pin_xy("D10")[1]), "HC-SR04 ECHO", SYM["D10"])


def leds(s):
    for c0, pin, kind, color, glow, n, to in (
            (8, "D3", "red", "#e53935", "#ff8a80", 7, "red LED (near)"),
            (18, "D5", "blue", "#1e88e5", "#82b1ff", 11, "blue LED (medium)"),
            (28, "D6", "green", "#43a047", "#b9f6ca", 15, "green LED (far)")):
        p = pin_xy(pin)
        t = hole(c0, "f")
        s.uno_wire(kind, n, pin, [(BEND[pin], p[1]), (BEND[pin], LANE[pin]), (t[0], LANE[pin]), t],
                   ({"D3": 700, "D5": 880, "D6": 1060}[pin], LANE[pin]), to, SYM[pin])
        s.resistor(c0, c0 + 4, "g", "220 Ω", R220)
        s.badge(n + 1, (cx(c0 + 2), ROW["g"] + 22), kind)
        s.led(c0 + 4, "i", color, glow)
        s.badge(n + 2, (cx(c0 + 6) + 6, ROW["i"]), kind)
        a = hole(c0 + 5, "j")
        s.wire("gnd", n + 3, [a, hole(c0 + 5, "B-")], (a[0] + 16, BY + 350))
    s.tag(cx(19) + 10, ROW["i"] + 26, "code: yellowLed", 9, "#4a148c")


LED_STEPS = [
    ("Red LED (near, ≤ 5 cm)", [
        ("7", "Uno D3 → column 8"), ("8", "220 Ω: column 8 → column 12"),
        ("9", "LED long leg (+) column 12, short leg 13"), ("10", "column 13 → − rail")]),
    ("Blue LED (medium) — yellowLed in the code", [
        ("11", "Uno D5 → column 18"), ("12", "220 Ω: column 18 → column 22"),
        ("13", "LED long leg (+) column 22, short leg 23"), ("14", "column 23 → − rail")]),
    ("Green LED (far)", [
        ("15", "Uno D6 (PWM) → column 28"), ("16", "220 Ω: column 28 → column 32"),
        ("17", "LED long leg (+) column 32, short leg 33"), ("18", "column 33 → − rail")]),
]
BASE_STEPS = [
    ("Power", [("1", "Uno 5V → bottom + rail"), ("2", "Uno GND → bottom − rail")]),
    ("HC-SR04 (top half, columns 42-45)", [
        ("3", "VCC → + rail"), ("4", "GND → − rail"), ("5", "TRIG ← Uno D9"), ("6", "ECHO → Uno D10")]),
]


# ---------------------------------------------------------------- v1 + v2: three LEDs
def sheet_v1_v2():
    s = Sheet("proximity-alert v1 + v2 — breadboard wiring",
              "Arduino Uno + HC-SR04 + 3 LEDs · ≤ 5 cm: red · 5-15 cm: blue blinks · > 15 cm: green · "
              "pins from v1-simple.ino · v2: same wiring as v1 (assumed; not visible in footage)", 1270)
    s.breadboard()
    s.uno({"5V", "GND", "D9", "D10", "D3", "D5", "D6"})
    power_and_sensor(s)
    leds(s)
    x, y = pin_xy("D11")
    s.add(f'<path d="M{x + 6},{y} L{x + 60},{y} L{x + 60},{BY - 22}" fill="none" stroke="#a35a00" stroke-width="1.5" '
          f'stroke-dasharray="4 3"/>')
    s.tag(x + 66, BY - 18, "D11 = motorPin in the code: leave it empty in v1/v2 (the fan is wired in the final build)",
          11, "#a35a00", "start")
    s.panel(BY + 500, BASE_STEPS + LED_STEPS, [
        "Why 220 Ω: it keeps each LED near (5 V − 2 V) / 220 Ω ≈ 14 mA; an Uno pin is rated 20 mA. LED long leg = + (anode), "
        "short leg goes to the − rail.",
        "v1 and v2 differ only in code (v2: averaging filter, faster blink when closer, green \"breathes\"). v2's pin lines were not "
        "visible in the video, so v2 is assumed to use these pins.",
        "Both sketches already switch D11 (motorPin) at ≤ 5 cm. The propeller fan was added in the final build: see "
        "wiring-final-fan.png. Power comes from the USB cable; top rails are not used.",
    ])
    s.save(HERE / "wiring-v1-v2.svg", ["../v1-simple/v1-simple.ino", "../v2-advanced/v2-advanced.ino"],
           free=[{"symbols": ["motorPin"], "uno": "D11", "why": "the fan belongs to the final build (owner's order: v1/v2 = LEDs)"}])


# ---------------------------------------------------------------- final: propeller fan, speed by zone
def sheet_final():
    s = Sheet("proximity-alert FINAL — propeller fan",
              "Fan speed follows the zone: red (≤ 5 cm) = fan stops · blue (5-15 cm) = fast · green (> 15 cm) = slow · "
              "pins: same wiring as v1 (assumed; not visible in footage)",
              1420,
              "Fan driver = RECOMMENDED parts (TIP120, 1N4007, 4×AA): the driver on the original breadboard is not legible "
              "in the recordings.")
    s.breadboard()
    s.uno({"5V", "GND", "D9", "D10", "D3", "D5", "D6", "D11"})
    power_and_sensor(s)
    leds(s)
    # D11 lands in the top half; the 1 kΩ base resistor crosses the centre gap
    s.between_rows("pwm", 19, "D11", FAN_B, "c", (cx(24), pin_xy("D11")[1]), "1 kΩ → TIP120 base (motor speed, PWM)",
                   SYM["D11"])
    s.resistor_v(FAN_B, "1 kΩ", R1K)
    s.badge(20, (cx(FAN_B) - 18, BY + 210), "pwm")
    s.tip120(FAN_B, "g", "TIP120*")
    s.badge(21, (cx(FAN_B) - 24, ROW["h"] + 6), "pwm")
    s.wire("gnd", 22, [hole(FAN_B + 2, "j"), hole(FAN_B + 2, "B-")], (cx(FAN_B + 2) + 16, BY + 350))
    s.diode(FAN_B + 1, FAN_B + 5, "i")
    s.badge(23, (cx(FAN_B + 6) + 6, ROW["i"]), "gnd")
    # motor + battery below the board
    my = BY + 470
    xm, xp = cx(FAN_B + 1) - 10, cx(FAN_B + 5) + 10
    s.motor(xm - 14, xp + 14, my, "small DC motor + propeller = fan", "speed: stop / fast / slow (PWM on D11)")
    for col, c, sx in ((FAN_B + 1, "#212121", xm), (FAN_B + 5, "#c62828", xp)):
        x, y = hole(col, "j")
        s.add(f'<path d="{rounded([(sx, my + 4), (sx, y + 12), (x, y + 12), (x, y)], 4)}" fill="none" stroke="{c}" '
              f'stroke-width="3.5" stroke-linecap="round"/>')
        s.pinhead(x, y)
    s.badge(24, (cx(FAN_B + 3), BY + 452), "gnd")
    plus, minus = s.battery(cx(FAN_B + 8) - 2, BY + 470, "4×AA (6 V)* — fan only")
    x, y = hole(FAN_B + 5, "g")
    s.wire("bat", 25, [plus, (plus[0], y + 10), (x, y + 10), (x, y)], (plus[0], BY + 440))
    b = hole(63, "B-")
    s.wire("gnd", 26, [minus, (minus[0], BY + 410), (b[0], BY + 410), b], (minus[0], BY + 440))
    s.panel(BY + 640, BASE_STEPS + LED_STEPS + [
        ("Fan driver — * recommended parts", [
            ("19", "Uno D11 → column 50 (top half)"), ("20", "1 kΩ across the centre gap, column 50"),
            ("21", "TIP120 printed side toward you: B=50, C=51, E=52"), ("22", "emitter column 52 → − rail"),
            ("23", "1N4007: column 51 → 55, stripe at 55"), ("24", "motor: black lead column 51, red lead 55"),
            ("25", "battery + → column 55"), ("26", "battery − → − rail (shared GND)")]),
    ], [
        "* Recommended, not seen: an Uno pin gives 20 mA, a propeller motor needs a few hundred mA, so the pin only drives the "
        "TIP120 (via 1 kΩ ≈ 3.6 mA) and the transistor switches the motor.",
        "The 1N4007 catches the motor's switch-off voltage spike. The motor runs from its own battery; only the grounds are "
        "joined. Match the battery to your motor's rated voltage.",
        "Speed = analogWrite(D11, …): stop / fast / slow values are set at the top of final-fan.ino. A logic-level MOSFET "
        "(e.g. IRLZ44N) can replace the TIP120. Top rails are not used.",
    ])
    s.save(HERE / "wiring-final-fan.svg", ["../final-fan/final-fan.ino"])


if __name__ == "__main__":
    sheet_v1_v2()
    sheet_final()
