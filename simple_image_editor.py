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
    image.save(bio, format='PNG')

    window['-IMAGE-'].update(data=bio.getvalue())


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
logo_col = Pg.Column([[Pg.Image('alatoo_logo.png')]])

layout = [[logo_col, control_col, image_col]]

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

    if event == '-SAVE-':
        save_path = Pg.popup_get_file(
            'Save', save_as=True, no_window=True
        ) + '.png'
        image.save(save_path, 'PNG')

window.close()
