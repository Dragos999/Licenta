import cv2

# Încarcă imaginea originală (de exemplu 1920x1080)
image = cv2.imread('C:/Users/mihae/OneDrive/Desktop/temp/ss.png')

# Dimensiunea dorită (de exemplu 800x600)
new_width = 1920
new_height = 1080

# Redimensionează imaginea
resized_image = cv2.resize(image, (new_width, new_height))

# Salvează imaginea rezultată
cv2.imwrite('C:/Users/mihae/OneDrive/Desktop/temp/ss_schimbat.png', resized_image)