import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.midi

pygame.init()

pygame.midi.init()

on_leds = []


def scan_launchpads():
    inputs = []
    outputs = []
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r
                
        if "Launchpad" in str(name):
            if input:
                inputs.append([str(name)[2:][:-1], i])

            if output:
                outputs.append([str(name)[2:][:-1], i])

        else:
            pass
        
    return inputs, outputs


def connect(connecttype, input_ch=0, output_ch=0):
    global input_device
    global output_device

    if connecttype == "manual":
        input_device = pygame.midi.Input(input_ch)
        output_device = pygame.midi.Output(output_ch)

    else:
        input_device = pygame.midi.Input(scan_launchpads()[0][0][1])
        output_device = pygame.midi.Output(scan_launchpads()[1][0][1])


def detect_press():
    try:
        if input_device.poll():
            midi_events = input_device.read(10)[0][0]

            return [midi_events[1], midi_events[2]]

    except:
        raise IndexError("Device not detected or not connected properly. Use pythonpad.connect() first")


def light_on(button, channel, color):
    output_device.note_on(button, color, channel - 1)
    on_leds.append(button)


def light_off(button, channel):
    if button in on_leds:
        output_device.note_off(button, 0, channel - 1)
        while button in on_leds:
            on_leds.remove(button)
