# raspberry-pi-fire-control 🔥🧯
This project is about a RaspberryPi 3 that is used as a fire alarm control panel.

## First
There is also an explanatory video for this project and a demonstration on YouTube. [Check it out](https://youtube.com/EasyTec100)

## The following components are required:
- 1x RaspberryPi (3b+) [other models will certainly work as well].
- 2x push button
- 1x buzzer
- 1x LED (red)
- 1x resistor 150 ohms

## What do I need to set?
Only the variables for the PIN assignment must be set correctly. 
More information can be found in the following table:

|        Variables             | Description                                         |
| ---------------------------- | --------------------------------------------------- |
|PIN_output_BUZ                | Pin of the buzzer (plus)                            |
|PIN_output_LED                | Pin of the LED (plus)                               |
|PIN_b_alarm                   | Pin of the alarm button                             |
|PIN_b_reset                   | Pin of the mute/reset button                        |

## How must it be connected
see connection diagram
![connection diagram](https://github.com/EasyTecRepository/raspberry-pi-fire-control/blob/main/pictures/pi_bmz_Steckplatine.png)
