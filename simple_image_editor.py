import PySimpleGUI as Pg
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO


# creating GUI functions and setting up the cases
def update_image(original_one, blur, contrast, emboss, contour, mirror, flip):
    """
    turning the "image" into a global variable,
    for we used it in the outer scope
    """
    global image
    image = original_one.filter(ImageFilter.GaussianBlur(blur))
    image = image.filter(ImageFilter.UnsharpMask(contrast))

    if emboss:
        image = image.filter(ImageFilter.EMBOSS())
    if contour:
        image = image.filter(ImageFilter.CONTOUR())

    if mirror:
        image = ImageOps.mirror(image)
    if flip:
        image = ImageOps.flip(image)

    """
    adapting the original image
    so our window stays the same regardless of its og size
    """
    image.thumbnail((400, 400))
    # creating a free space in RAM, so we are able to work with the image
    bio = BytesIO()

    # error handling
    try:
        image.save(bio, format='PNG')
    except ValueError:
        print('Just click on "close".')

    window['-IMAGE-'].update(data=bio.getvalue())


# creating another window with "about" and "copyright" sections
def additional_window():
    layout_new = [
        [Pg.Text("About: A simple image editor. You can flip, mirror "
                 "and do other fun stuff with your image. "
                 "if you choose other image format other than 'png' "
                 "an error might occur, "
                 "so in that case just click on 'Close' "
                 "button and you will be able to edit that image. \n"
                 "Copyright: © \n"
                 "Year of publication: 2022. \n"
                 "Owner: @cutesytee / Henry Ernestov. \n"
                 "Some rights reserved:\n"
                 "You can do whatever you want with this code.\n"
                 "Just give me credits :p. ",
                 size=(50, 20), key='-TEXT-')]
    ]

    window = Pg.Window("About and Copyright", layout_new)

    while True:
        event, values = window.read()
        if event == Pg.WINDOW_CLOSED:
            break
        additional_window()
        window['-TEXT-'].update()

    window.close()


# adding an attractive theme
Pg.theme('Purple')

# letting the user choose an image
image_path = Pg.popup_get_file('Open', no_window=True)

# creating the look of GUI
control_col = Pg.Column([
    [Pg.Frame('Blur', layout=[[Pg.Slider(range=(0, 10),
              orientation='h', key='-BLUR-')]])],
    [Pg.Frame('Contrast', layout=[[Pg.Slider(range=(0, 10),
              orientation='h', key='-CONTRAST-')]])],

    [Pg.Checkbox('Emboss', key='-EMBOSS-'),
        Pg.Checkbox('Contour', key='-CONTOUR-')],
    [Pg.Checkbox('Mirror', key='-MIRROR-'),
        Pg.Checkbox('Flip', key='-FLIPY-')],
    [Pg.Button("Choose another image", key="-CHOOSING-")],
    [Pg.Button('Save image', key='-SAVE-')]
])

image_col = Pg.Column([[Pg.Image(image_path, key='-IMAGE-')]])
"""
getting the logo of our uni from your files.
make sure to download it from the git repository
"""
logo_and_about_col = Pg.Column([
    [Pg.Image('alatoo_logo.png')],
    [Pg.Button('About and Copyright', key="-ABOUT-")]
])

layout = [[logo_and_about_col, control_col, image_col]]

original = Image.open(image_path)
window = Pg.Window('Image Editor', layout)

while True:
    event, values = window.read(timeout=50)
    if event == Pg.WIN_CLOSED:
        break

    # updating everything above with "keys" we created
    update_image(
        original,
        values['-BLUR-'],
        values['-CONTRAST-'],
        values['-EMBOSS-'],
        values['-CONTOUR-'],
        values['-MIRROR-'],
        values['-FLIPY-'])

    if event == "-CHOOSING-":
        image_path = Pg.popup_get_file('Open', no_window=True)

    if event == "-ABOUT-":
        additional_window()

    if event == '-SAVE-':
        save_path = Pg.popup_get_file(
            'Save', save_as=True, no_window=True
        ) + '.png'
        image.save(save_path, 'PNG')

window.close()
