import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.midi
from pygame.locals import *
from win32 import *

pygame.init()
pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post

pygame.midi.init()


def scan_launchpads():
    pygame.midi.init()
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
    #pygame.midi.quit()
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

connect("auto")

while True:
    buttons = detect_press()
    if buttons != None:
        print(buttons)
