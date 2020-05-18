from Optris import *

# Init camera
evo_irimager_usb_init()

# Get frame size
size = evo_irimager_get_thermal_image_size()

# Grab an image
img = evo_irimager_get_thermal_image(*size)

# Convert from raw counts -> degrees
img = raw_to_C(img)

# Print some stats
print(img.mean(), img.min(), img.max())

# Show the image
import matplotlib.pyplot as plt
plt.imshow(img)
plt.show()


if __name__ == '__main__':
    print('ok')