import sys
import PySimpleGUI as sg
from time import time
sg.theme('DarkBlue15')
setupLayout = [[sg.Input(size = (10,1), key='-TIME-'), sg.Spin(['Hours', 'Minutes', 'Seconds'], key='-SPIN-')],
               [sg.Input(size = (10,1),key='-QUESTIONS-'), sg.Text('Questions')],
               [sg.Button('Enter', key = '-ENTER-')]
               ]
warningLayout = [[sg.Text('', key='-WARNING_TEXT-')], [sg.Button('OK', key='-WARNING_BUTTON-')]]
setupPage = sg.Window('Setup Page', setupLayout)

while True:

    event, values = setupPage.read()
    if event == sg.WIN_CLOSED:
        sys.exit(0)
    if event == '-ENTER-':
        try:
            global hours
            global minutes
            global seconds
            global milliseconds
            global questions

            time1 = float(values['-TIME-'])
            questions = int(values['-QUESTIONS-'])
            unit = values['-SPIN-']
            temp = 0
            match unit:
                case 'Hours':
                    temp = time1 * 3600
                case 'Minutes':
                    temp = time1 * 60
                case 'Seconds':
                    temp = time1
            global finalTime
            finalTime = temp
            milliseconds = int((temp-int(temp))*100)
            seconds = int(temp)%60
            minutes = int((int(temp)/60)%60)
            hours = int((int(temp)/60)/60)

            setupPage.close()
            break
        except:
            if values['-TIME-'].isnumeric():
                sg.Window('Warning', [[sg.Text('INVALID QUESTIONS INPUT', key='-WARNING_TEXT-')]],auto_close=True,auto_close_duration=4).read(timeout=1)
            else:
                sg.Window('Warning', [[sg.Text('INVALID TIME INPUT', key='-WARNING_TEXT-')]],auto_close=True,auto_close_duration=4).read(timeout=1)
timerLayout = [
    [sg.Text('',key='-MAINTIMER_TEXT-',text_color = 'blue',
    background_color = 'green', pad = (5,5),auto_size_text = True, expand_x=True)],
    [sg.Text('',pad = (5,5),key='-PER_QUESTIONS_TEXT-',auto_size_text= True, expand_x=True)],
    [sg.Button('Question Finished',button_color = ('blue','green'), pad = (5,5), key='-QUESTION_FINISHED_BUTTON-', expand_x=True), sg.Button('Start',button_color = ('white','green'), pad = (5,5), key='-STARTSTOP-', expand_x=True)]
]
timerPage = sg.Window('Timer',timerLayout,size=(500,500))


while True:
    event, values = timerPage.read()
    if event == sg.WIN_CLOSED:
        sys.exit(0)
    if event == '-STARTSTOP-':
        break
timerPage['-STARTSTOP-'].update('Stop', button_color=('white', 'red'))
active = True
startTime = time()
questionStartTime = startTime
check = True
while True:
    global totalTime
    global questionTime
    global stopTime
    event, values = timerPage.read(timeout=10)

    if event == sg.WIN_CLOSED:
        sys.exit(0)
    if event == '-QUESTION_FINISHED_BUTTON-':
        try:
            questionStartTime = time()
            questions -= 1
            timerPerQ = ((hours * 3600 + minutes * 60 + seconds) - totalTime) / questions
            timerPerQM = int(timerPerQ / 60)
            timerPerQS = int(timerPerQ % 60)
        except: pass
    if event =='-STARTSTOP-':
        active = not active
        if active:
            startTime += time() - stopTime
            questionStartTime += time() - stopTime
            timerPage['-STARTSTOP-'].update('Stop', button_color=('white', 'red'))
        else:
            stopTime = time()
            timerPage['-STARTSTOP-'].update('Start', button_color=('white', 'green'))
    if active:
        totalTime = time() - startTime
        totalMilliseconds = int((totalTime - int(totalTime))*100)
        totalHours = int((totalTime/60)/60)
        totalMinutes = int((totalTime/60)%60)
        totalSeconds = int(totalTime%60)
        questionTime = time() - questionStartTime
        questionMilliseconds = int((questionTime - int(questionTime)) * 100)
        questionHours = int((questionTime / 60) / 60)
        questionMinutes = int((questionTime / 60) % 60)
        questionSeconds = int(questionTime % 60)

        if check:
            timerPerQ = ((hours*3600 + minutes*60 + seconds) - totalTime) / questions
            timerPerQM = int(timerPerQ/60)
            timerPerQS = int(timerPerQ%60)
            check = False
        timerPage['-MAINTIMER_TEXT-'].update(f'{totalHours}hrs {totalMinutes}mins {totalSeconds}s and {totalMilliseconds}ms /{hours}hrs {minutes}mins {seconds}s and {milliseconds}ms')
        timerPage['-PER_QUESTIONS_TEXT-'].update(f'{questionHours}hrs {questionMinutes}mins {questionSeconds}s and {questionMilliseconds}ms/{timerPerQM}mins and {timerPerQS}s')
    if questions == 0:
        timerPage.close()
        break

endPage = sg.Window('',[[sg.Text('Test Over')],[sg.Text(f'Test Completed in {totalHours} hrs, {totalMinutes} mins, {totalSeconds} secs, and {totalMilliseconds} millis')]])
while True:
    event, values = endPage.read()
    if event == sg.WIN_CLOSED:
        sys.exit(0)













