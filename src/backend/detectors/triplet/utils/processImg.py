from PIL import Image
import numpy as np

def resize_and_pad(img, tgt_size, padding_value=255):
    old_size = img.size
    ratio = float(tgt_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])

    img = img.resize(new_size, Image.ANTIALIAS)
    # create a new image and paste the resized on it

    new_img = Image.new("L", (tgt_size, tgt_size), color=padding_value)
    # copy the original image to the center
    new_img.paste(img, ((tgt_size-new_size[0])//2,
                        (tgt_size-new_size[1])//2))
    return new_img


def preprocess_img(cv_img, tgt_size, padding_value=255):
    try:
        resized_img = resize_and_pad(Image.fromarray(cv_img).convert('L'), tgt_size, padding_value)
    except:
        cv_img = cv_img.astype(np.uint8)
        resized_img = resize_and_pad(Image.fromarray(cv_img).convert('L'), tgt_size, padding_value)
    return resized_img.convert('RGB')