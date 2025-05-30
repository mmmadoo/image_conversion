from PIL import Image,ExifTags
import os

# ファイルが複数選択された際に、それらを縦に連結する
def image_combination(alist):
    img_width = alist[0].width
    img_height = 0
    for file in alist:
        img_height += file.height
    
    img = Image.new('RGB',(img_width,img_height))

    update_height = 0
    for i in range(len(alist)):
        img.paste(alist[i],(0,update_height))
        update_height += alist[i].height
        
    return img

# 変換前のファイルをフォルダから削除する
def delete_before_file(name_alist):
    for name in name_alist:
        os.remove(name)

# ファイルをストリームとして送信
def generate(file_path):
    with open(file_path,'rb') as f:
        yield from f

#ファイルのExif情報から画像ファイルの向きを修正する
def correct_image_orientation(img):
    try:
        exif = img._getexif()
        if exif is not None:
            orientation = None
            for key in ExifTags.TAGS.keys():
                if ExifTags.TAGS[key] == 'Orientation':
                    orientation = key
                    break
            if orientation is not None:
                orientation_value = exif.get(orientation,None)
                if orientation_value == 3:
                    img = img.rotate(180,expand = True)
                elif orientation_value == 6:
                    img = img.rotate(270,expand = True)
                elif orientation_value == 8:
                    img = img.rotate(90,expand = True)
    except Exception:
        pass
    return img

#ファイルの向きを修正して、保存する
def save_uploaded_image(file,file_name):
    img = Image.open(file)
    img = correct_image_orientation(img)
    img.save(file_name)
