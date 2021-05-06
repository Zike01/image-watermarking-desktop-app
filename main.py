from PIL import Image, ImageTk, ImageDraw, ImageFont
import PIL.Image  # Import the image MODULE for opening images

from tkinter import *
from tkinter import filedialog, simpledialog, messagebox

# -----------------------CONSTANTS ---------------------------#
WHITE = (255, 255, 255, 128)
BLACK = (0, 0, 0, 128)
filename = None
# ------------------------------------------------------------#


def add_watermark(image_path, text_color):
    """
    Places a watermark on the selected image.
    """

    # Ask the user for watermark text
    text = simpledialog.askstring(title="Watermark Text",
                                  prompt="Enter watermark text")

    # Add watermark to the image if text was entered
    if text:
        with PIL.Image.open(image_path).convert("RGBA") as im:

            # Get the dimensions of the imported image
            [width, height] = im.size

            # make a blank image for the text, initialized to transparent text color
            txt = PIL.Image.new("RGBA", im.size, (255, 255, 255, 0))

            # get a font
            fnt = ImageFont.truetype("arial.ttf", 40, encoding="unic")
            # get a drawing context
            d = ImageDraw.Draw(txt)

            # draw text at centre of the image
            d.text((width/2, height/2), text, font=fnt, fill=text_color)

            out = PIL.Image.alpha_composite(im, txt)

            out = out.convert("RGB")

            # Save the watermarked image to the watermarked_images folder
            out.save(f"watermarked_images/{image_path.split('/')[-1]}")

        # Tell the user that image has been saved
        messagebox.showinfo(title="Image Saved", message="Your watermarked image has been saved.")


def select_image():
    """
    Opens a dialog box for the user to select an image.
    """
    global filename
    filename = filedialog.askopenfilename(title='Select Image', filetypes=[
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ])

    with PIL.Image.open(filename).convert("RGBA") as im:
        # Get the dimensions of the imported image
        [width, height] = im.size

        # If the image is too large, halve the width and height
        if height >= 1000:
            im = im.resize((int(width / 2), int(height / 2)))

        # Place the imported image on the panel label
        image = ImageTk.PhotoImage(im)
        panel.configure(image=image)
        panel.image = image


def on_option_change(event):
    """
    Changes the add_watermark parameters when listbox value is changed.
    """
    if variable.get() == "White Text":
        add_watermark_button.config(command=lambda: add_watermark(filename, WHITE))
    else:
        add_watermark_button.config(command=lambda: add_watermark(filename, BLACK))


# -----------------------UI SETUP ---------------------------#
window = Tk()
window.title("Image Watermarking Desktop App")
window.config(padx=20, pady=20)

# Show a maximized window with the window title still visible
window.state("zoomed")

# Labels
panel = Label(window, text=" ")
panel.grid(row=0, column=0, columnspan=3)

# Buttons
select_image_button = Button(text="Select Image", command=select_image)
select_image_button.grid(row=1, column=0)

add_watermark_button = Button(text="Add Watermark", command=lambda: add_watermark(filename, WHITE))
add_watermark_button.grid(row=1, column=1)

# Listbox
variable = StringVar(window)
variable.set("White Text")  # default value
options = OptionMenu(window, variable, "White Text", "Black Text", command=on_option_change)
options.grid(row=1, column=2)

window.mainloop()
