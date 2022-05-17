import cv2
import numpy as np
from Utils import *
from Sudoku_solver import *
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import messagebox

image_path = ''
HEIGHT, WIDTH = 450, 450

def makeCenter(root):
    '''
    Place the window in the center of the screen
    input:
        root: tkinter object
    return:
        None
    '''
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth()//2) - (width//2)
    y = (root.winfo_screenheight()//2) - (height//2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def choose_image():
    '''
    Choose an image from file explorer
    input:
        None
    return:
        None
    '''
    global image_path
    image_path = filedialog.askopenfilename()
    if len(image_path)>0:
        image_path_label.config(text=image_path, foreground='green')
        image = ImageTk.PhotoImage(Image.open(image_path).resize((HEIGHT, WIDTH)))
        image_canvas.create_image(0,0, anchor=NW, image=image) 
        image_canvas.image = image
    else:
        image_path_label.config(text='Choose image', foreground='red')

def solve_sudoku():
    '''
    Solve sudoku matrix in the image
    Input:
        None
    Output:
        None
    '''

    # Check if user have chosen the image
    if len(image_path)>0:
        # Load an preprocess the image
        image = cv2.imread(image_path)
        image = cv2.resize(image, (WIDTH, HEIGHT))
        image_threshold = preprocess(image)

        # Find biggest countours in the image => Sudoku matrix
        countours, _ = cv2.findContours(image_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        biggest, _ = biggest_countour(countours)

        if biggest.size != 0:
            biggest = reorder(biggest)
            points_1 = np.float32(biggest)
            points_2 = np.float32([[0, 0], [WIDTH, 0], [0, HEIGHT], [WIDTH, HEIGHT]])
            matrix = cv2.getPerspectiveTransform(points_1, points_2)
            image_warp_colored = cv2.warpPerspective(image, matrix, (WIDTH, HEIGHT))
            image_result = image_warp_colored.copy()
            image_warp_colored = cv2.cvtColor(image_warp_colored, cv2.COLOR_BGR2GRAY)
            boxes = split_boxes(image_warp_colored)
            model = initialize_prediction_model()
            numbers = get_prediction(boxes, model)

            numbers = np.reshape(np.array(numbers), (9, 9))
            numbers, state = solve_Sudoku(numbers, 0, 0)
            numbers = list(np.reshape(numbers, (1, -1))[0])
            
            if state:
                image_result = display_numbers(image_result, numbers, color=(255, 0, 0))
                cv2.imshow('Solved', image_result)
            else:
                image_result = display_numbers(image_result, numbers, color=(255, 255, 0))
                cv2.imshow('Unable to solve', image_result)

        else:
            print('hahahahaha========================================')
    else:
        messagebox.showerror('Error', 'Please choose an image that contain Sudoku')

root = Tk()
root.title('Sudoku solver')
root.geometry('600x600')
makeCenter(root)
root.resizable(width = False, height = False)

label = Label(root, text='Sudoku solver', font=(10))
label.pack()

button_frame = Frame(root)
choose_image_button = Button(button_frame, width=15, text='Choose image', command=choose_image)
choose_image_button.pack(side=LEFT)
solve_button = Button(button_frame, width=15, text='Solve Sudoku', command=solve_sudoku)
solve_button.pack(side=RIGHT)
button_frame.pack(pady=10)
image_path_label = Label(root,width=50)
image_path_label.pack()
    
image_frame = Frame(root)
image_canvas = Canvas(image_frame, width=WIDTH, height=HEIGHT)
image_canvas.pack()
image_frame.pack()

root.mainloop()