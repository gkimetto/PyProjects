import tkinter

# Handler for timer event


def alarm():
    print ("Calling Pizza Company.")

# Handler for ringing doorbell


def doorbell():
    print ("Ding Dong!!")
    print ("Opening the door!! ")

# Handler for when the phone rings


def phonecall():
    print ("Answering the phone.")

# Create buttons and assign callbacks
root = tkinter.Tk()
tkinter.Button(root, text='Ring Doorbell', command=doorbell).pack()
tkinter.Button(root, text='Call Phone', command=phonecall).pack()

# Set a timer for 1 second

root.after(4000, alarm)

# Start the event loop

root.mainloop()

