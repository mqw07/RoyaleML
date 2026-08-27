from computer_vision.computer_vision import grab_frame, capture_elixir
from classifications.identification import identify

def test_elixir_grabbing():
    eframe = grab_frame(capture_elixir)
    e_count = identify.grab_elixir(eframe)
    assert e_count == 6