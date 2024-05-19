import base64

# Read image file
with open('./static/logo.png', 'rb') as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

with open('newimage.png', 'wb') as file:
    file.write(base64.b64decode(str(encoded_string)))

print("Encoded string saved in 'encoded_image.txt'.")