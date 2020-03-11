import cv2

IMG_DIR = "C:/Users/curti/OneDrive/Documents/Python Scripts/Google Search History/SavedGraphs"

fourcc = cv2.VideoWriter_fourcc(*'XVID')

out = cv2.VideoWriter(f'{IMG_DIR}/vid.avi',fourcc, 5.0, (1200,700))

for i in range(388):
    img_path = f'{IMG_DIR}/{i}.png'
    frame = cv2.imread(img_path)
    out.write(frame)
out.release()
print('*************')
print('Video Created')
print('*************')