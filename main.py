import platform
import httpx
import sys
from rich import print
from rich.console import Console
from LocationHandler import macOS_queryLocation


def runtimeError(str):
    raise RuntimeError(str)


if platform.system() != "Darwin":
    runtimeError(
        "Error! This program is not cross-platform, and only works on macos. Implement your own LocationHandler if you care")


console = Console()


def get_api_key():
    API_KEY_DIR = R"./.API_KEY"
    try:
        with open(API_KEY_DIR, 'r', encoding='ascii') as file:
            api_key = file.read().strip()
    except FileNotFoundError:
        runtimeError(
            f"Error: You are missing the '{API_KEY_DIR}'"
            f". Check readme for instructions on how to get one."
        )
        return None
    except Exception as e:
        runtimeError(f"An unspecified error occurred: {e}")
    return api_key


class GWeatherRequestPool:
    api_key = get_api_key()
    latitude, longitude, confidence = macOS_queryLocation()
    json_dict: dict = {}
    requests = []

    def __init__(self):
        if self.latitude is None or self.longitude is None:
            runtimeError("Unable to get location!")

    def makeRequest(self, request: str):
        self.requests.append(request)
        console_status = (
            f"[blue][i]"
            f"Calling weather.googleapis.com/v1/{request}..."
            f"[/blue][/i]")

        url: str = (
            f"https://weather.googleapis.com/v1/{request}:lookup?"
            f"key={self.api_key}&"
            f"location.latitude={self.latitude:.4}&"
            f"location.longitude={self.longitude:.4}"
        )
        with console.status(console_status, spinner="dots"):
            with httpx.Client(timeout=10.0) as client:
                response = httpx.get(url)
                response.raise_for_status()
                try:
                    json_dict_partial: dict = response.json()
                except ValueError:
                    runtimeError(
                        f"Expected JSON, got: {
                            response.headers.get('content-type')}"
                        f":\n{response.text[:500]}")
        self.json_dict = self.json_dict | json_dict_partial


class Result:
    def __init__(self, pool):
        data = pool.json_dict
        for request in pool.requests:
            if request == "currentConditions":
                self.timezone = data.get("timeZone").get("id")
                self.temp_c = data.get("temperature").get("degrees")
            elif request == "forecast/days":
                self.max_c = data.get("forecastDays")[0].get(
                    "maxHeatIndex").get("degrees")


ansiColorNames = {0: "black",
                  1: "red",
                  2: "green",
                  3: "yellow",
                  4: "blue",
                  5: "magenta",
                  6: "cyan",
                  7: "white",
                  8: "bright_black",
                  9: "bright_red",
                  10: "bright_green",
                  11: "bright_yellow",
                  12: "bright_blue",
                  13: "bright_magenta",
                  14: "bright_cyan",
                  15: "bright_white",
                  16: "grey0",
                  17: "navy_blue",
                  18: "dark_blue",
                  20: "blue3",
                  21: "blue1",
                  22: "dark_green",
                  25: "deep_sky_blue4",
                  26: "dodger_blue3",
                  27: "dodger_blue2",
                  28: "green4",
                  29: "spring_green4",
                  30: "turquoise4",
                  32: "deep_sky_blue3",
                  33: "dodger_blue1",
                  36: "dark_cyan",
                  37: "light_sea_green",
                  38: "deep_sky_blue2",
                  39: "deep_sky_blue1",
                  40: "green3",
                  41: "spring_green3",
                  43: "cyan3",
                  44: "dark_turquoise",
                  45: "turquoise2",
                  46: "green1",
                  47: "spring_green2",
                  48: "spring_green1",
                  49: "medium_spring_green",
                  50: "cyan2",
                  51: "cyan1",
                  55: "purple4",
                  56: "purple3",
                  57: "blue_violet",
                  59: "grey37",
                  60: "medium_purple4",
                  62: "slate_blue3",
                  63: "royal_blue1",
                  64: "chartreuse4",
                  66: "pale_turquoise4",
                  67: "steel_blue",
                  68: "steel_blue3",
                  69: "cornflower_blue",
                  71: "dark_sea_green4",
                  73: "cadet_blue",
                  74: "sky_blue3",
                  76: "chartreuse3",
                  78: "sea_green3",
                  79: "aquamarine3",
                  80: "medium_turquoise",
                  81: "steel_blue1",
                  83: "sea_green2",
                  85: "sea_green1",
                  87: "dark_slate_gray2",
                  88: "dark_red",
                  91: "dark_magenta",
                  94: "orange4",
                  95: "light_pink4",
                  96: "plum4",
                  98: "medium_purple3",
                  99: "slate_blue1",
                  101: "wheat4",
                  102: "grey53",
                  103: "light_slate_grey",
                  104: "medium_purple",
                  105: "light_slate_blue",
                  106: "yellow4",
                  108: "dark_sea_green",
                  110: "light_sky_blue3",
                  111: "sky_blue2",
                  112: "chartreuse2",
                  114: "pale_green3",
                  116: "dark_slate_gray3",
                  117: "sky_blue1",
                  118: "chartreuse1",
                  120: "light_green",
                  122: "aquamarine1",
                  123: "dark_slate_gray1",
                  125: "deep_pink4",
                  126: "medium_violet_red",
                  128: "dark_violet",
                  129: "purple",
                  133: "medium_orchid3",
                  134: "medium_orchid",
                  136: "dark_goldenrod",
                  138: "rosy_brown",
                  139: "grey63",
                  140: "medium_purple2",
                  141: "medium_purple1",
                  143: "dark_khaki",
                  144: "navajo_white3",
                  145: "grey69",
                  146: "light_steel_blue3",
                  147: "light_steel_blue",
                  149: "dark_olive_green3",
                  150: "dark_sea_green3",
                  152: "light_cyan3",
                  153: "light_sky_blue1",
                  154: "green_yellow",
                  155: "dark_olive_green2",
                  156: "pale_green1",
                  157: "dark_sea_green2",
                  159: "pale_turquoise1",
                  160: "red3",
                  162: "deep_pink3",
                  164: "magenta3",
                  166: "dark_orange3",
                  167: "indian_red",
                  168: "hot_pink3",
                  169: "hot_pink2",
                  170: "orchid",
                  172: "orange3",
                  173: "light_salmon3",
                  174: "light_pink3",
                  175: "pink3",
                  176: "plum3",
                  177: "violet",
                  178: "gold3",
                  179: "light_goldenrod3",
                  180: "tan",
                  181: "misty_rose3",
                  182: "thistle3",
                  183: "plum2",
                  184: "yellow3",
                  185: "khaki3",
                  187: "light_yellow3",
                  188: "grey84",
                  189: "light_steel_blue1",
                  190: "yellow2",
                  192: "dark_olive_green1",
                  193: "dark_sea_green1",
                  194: "honeydew2",
                  195: "light_cyan1",
                  196: "red1",
                  197: "deep_pink2",
                  199: "deep_pink1",
                  200: "magenta2",
                  201: "magenta1",
                  202: "orange_red1",
                  204: "indian_red1",
                  206: "hot_pink",
                  207: "medium_orchid1",
                  208: "dark_orange",
                  209: "salmon1",
                  210: "light_coral",
                  211: "pale_violet_red1",
                  212: "orchid2",
                  213: "orchid1",
                  214: "orange1",
                  215: "sandy_brown",
                  216: "light_salmon1",
                  217: "light_pink1",
                  218: "pink1",
                  219: "plum1",
                  220: "gold1",
                  222: "light_goldenrod2",
                  223: "navajo_white1",
                  224: "misty_rose1",
                  225: "thistle1",
                  226: "yellow1",
                  227: "light_goldenrod1",
                  228: "khaki1",
                  229: "wheat1",
                  230: "cornsilk1",
                  231: "grey100",
                  232: "grey3",
                  233: "grey7",
                  234: "grey11",
                  235: "grey15",
                  236: "grey19",
                  237: "grey23",
                  238: "grey27",
                  239: "grey30",
                  240: "grey35",
                  241: "grey39",
                  242: "grey42",
                  243: "grey46",
                  244: "grey50",
                  245: "grey54",
                  246: "grey58",
                  247: "grey62",
                  248: "grey66",
                  249: "grey70",
                  250: "grey74",
                  251: "grey78",
                  252: "grey82",
                  253: "grey85",
                  254: "grey89",
                  255: "grey93",
                  }


HEAT_GRADIENT_MIN = 8
HEAT_GRADIENT_MAX = 36
heatGradient = {
    8:  "blue1",
    9: "dodger_blue3",
    10:  "light_sea_green",
    11: "cyan3",
    12: "medium_spring_green",
    13: "spring_green1",
    14: "spring_green2",
    15: "spring_green2",
    16: "spring_green2",
    17: "spring_green2",
    18: "spring_green3",
    19: "spring_green3",
    20: "spring_green3",
    21: "spring_green3",
    22: "spring_green3",
    23: "green1",
    24: "chartreuse1",
    25: "green_yellow",
    26: "yellow2",
    27: "yellow1",
    28: "gold1",
    29: "orange1",
    30: "dark_orange",
    31:  "orange_red1",
    32:  "red1",
    33:  "red1",
    34:  "red3",
    35:   "red3",
    36:    "dark_red"
}


def showGradient():
    print("Showing gradient:")
    color = heatGradient.get(8)
    print(f"[{color}] <8°C = {color}[/{color}]")

    for i in range(8, 37):
        color = heatGradient.get(i)
        print(f"[{color}]{i:>3}°C = {color}[/{color}]")

    color = heatGradient.get(36)
    print(f"[{color}]>36°C = {color}[/{color}]")

# expects heat in degrees celsius


def fmt_heat(deg_c: float):
    if deg_c < HEAT_GRADIENT_MIN:
        color = heatGradient.get(HEAT_GRADIENT_MIN)
    elif deg_c > HEAT_GRADIENT_MAX:
        color = heatGradient.get(HEAT_GRADIENT_MAX)
    else:
        color = heatGradient.get(round(deg_c))
    return (f"[{color}]{deg_c}°C[/{color}]")


usage_str = f"python {sys.argv[0]} [-g|--gradient] [-c|--coordinates]"


def main():
    PRINT_COORDINATES = False
    if len(sys.argv) == 2:
        if sys.argv[1] == "-g" or sys.argv[1] == "--gradient":
            showGradient()
            return
        elif sys.argv[1] == "-c" or sys.argv[1] == "--coordinates":
            PRINT_COORDINATES = True
        else:
            runtimeError(f"Unknown arguments passed.\nUsage:\t{usage_str}")
    elif len(sys.argv) != 1:
        runtimeError(f"Unknown arguments passed.\nUsage:\t{usage_str}")

    pool = GWeatherRequestPool()
    pool.makeRequest("currentConditions")
    pool.makeRequest("forecast/days")

    res = Result(pool)
    print(f"It is {fmt_heat(res.temp_c)} right now. "
          f"The highest today should be {fmt_heat(res.max_c)}.")
    if PRINT_COORDINATES:
        print(
            f"Coordinates: (lat={pool.latitude:.6},long={pool.longitude:.6})")


if __name__ == "__main__":
    main()
