import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


numbers = range(2,13)
rolls = list(np.zeros(11).astype('int'))
historyRolls=[]

def createBarGraph(numbers, rolls):
    fig = plt.figure(figsize =(25, 15))
    rects = plt.bar(numbers, rolls, color='red', width=0.4)
    plt.xticks(numbers, fontsize=20, weight = 'bold')
    plt.title('Dice Rolls', fontsize=14)
    plt.xlabel('Number', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.yticks([0,1],fontsize=20, weight = 'bold')
    plt.grid(visible=True, which='major', axis='y')
    fig.tight_layout()
    return fig, rects


def updateBarGraph(rolls, figure, rects):
    i=0
    for rect in rects:
        rect.set_height(rolls[i])
        i+=1
    plt.ylim([0, max(rolls)])
    plt.yticks(range(max(rolls)+1))
    fig.tight_layout()
    fig.canvas.draw()



def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


sg.theme('LightBlue')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Catan Dice Stats', font=("Helvetica", 25))],
            [sg.Text('Last 10 Rolls', key='-HISTORY-', font=("Helvetica", 50))],
            [sg.Canvas(key='-CANVAS-')],
            [sg.Input('', enable_events=True,  key='-INPUT-', )],
            [sg.Button('Submit', visible=False, bind_return_key=True)],
            [sg.Button('EXIT')] ]

# Create the Window
window = sg.Window('Catan Dice Counter', layout,finalize=True, element_justification='center', resizable=True)
#window.maximize()
fig, rects = createBarGraph(numbers,rolls)
draw_figure(window['-CANVAS-'].TKCanvas, fig)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'EXIT': # if user closes window or clicks cancel
        break
    if len(values['-INPUT-']) and values['-INPUT-'] not in ('123456789101112'):
        # delete last char from input
        window['-INPUT-'].update('')
    elif event == 'Submit':
        #print(int(window['-INPUT-'].get()) in numbers)
        if(window['-INPUT-'].get() != '' and int(window['-INPUT-'].get()) in numbers):
            print('You have submited %s'% window['-INPUT-'].get())
            rolls[int(window['-INPUT-'].get())-2]+=1
            historyRolls.append(int(window['-INPUT-'].get()))
            updateBarGraph(rolls, fig, rects)
            window['-INPUT-'].update('')
            window['-HISTORY-'].update('Last Ten Rolls' + str(historyRolls[-10:]))
        else:
            window['-INPUT-'].update('')

window.close()
