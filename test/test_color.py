from app.models.color import Color


def test_color_initialization():
    # Test proper initialization of a color object
    color = Color(100, 150, 200)
    assert color.r == 100
    assert color.g == 150
    assert color.b == 200


def test_color_initialization_with_clamping():
    # Test if values exceeding 255 are clamped
    color = Color(300, 500, 700)
    assert color.r == 255
    assert color.g == 255
    assert color.b == 255


def test_color_from_hex():
    # Test creating a color from a hex value
    color = Color.from_hex(0xFF0010)
    assert color.r == 255
    assert color.g == 0
    assert color.b == 16


def test_color_from_rgb():
    # Test creating a color using RGB values
    color = Color.from_rgb(10, 20, 30)
    assert color.r == 10
    assert color.g == 20
    assert color.b == 30


def test_color_random():
    # Test random color generation
    color = Color.random
    assert 0 <= color.r <= 255
    assert 0 <= color.g <= 255
    assert 0 <= color.b <= 255


def test_color_predefined_colors():
    # Test predefined colors
    assert Color.white.r == 255 and Color.white.g == 255 and Color.white.b == 255
    assert Color.black.r == 0 and Color.black.g == 0 and Color.black.b == 0
    assert Color.blue.r == 0 and Color.blue.g == 0 and Color.blue.b == 255
    assert Color.red.r == 255 and Color.red.g == 0 and Color.red.b == 0
    assert Color.green.r == 0 and Color.green.g == 255 and Color.green.b == 0
    assert Color.yellow.r == 255 and Color.yellow.g == 255 and Color.yellow.b == 0
    assert Color.magenta.r == 255 and Color.magenta.g == 0 and Color.magenta.b == 255
    assert Color.cyan.r == 0 and Color.cyan.g == 255 and Color.cyan.b == 255


def test_color_addition():
    # Test adding two colors
    color1 = Color(101, 102, 103)
    color2 = Color(110, 120, 130)
    result = color1 + color2
    assert result.r == 211
    assert result.g == 222
    assert result.b == 233


def test_color_addition_with_clamping():
    # Test adding two colors resulting in clamping
    color1 = Color(200, 200, 200)
    color2 = Color(100, 100, 100)
    result = color1 + color2
    assert result.r == 255
    assert result.g == 255
    assert result.b == 255


def test_color_hex_property():
    # Test getting the hex value of a color
    color = Color(255, 0, 255)
    assert color.hex == 0xFF00FF


def test_color_tuple():
    # Test getting the tuple value of a color
    color = Color(10, 20, 30)
    assert color.tuple == (10, 20, 30)
