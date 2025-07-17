import cv2
import numpy as np
import matplotlib.pyplot as plt

def dft2(img):
    M, N = img.shape
    dft_result = np.zeros((M, N), dtype=np.complex128)

    for u in range(M):
        for v in range(N):
            dft_sum = 0
            for x in range(M):
                for y in range(N):
                    dft_sum += img[x, y] * np.exp(-2j * np.pi * ((u * x / M) + (v * y / N)))
            dft_result[u, v] = dft_sum

    return dft_result

# Load the image in grayscale
path = r"C:\Users\Gurukumar\Pictures\Saved Pictures\wallpaperflare.com_wallpaper (1).jpg"
img = cv2.imread(path, 0)

# Perform the 2D Discrete Fourier Transform
dft_img = dft2(img)

# Shift the zero frequency component to the center
dft_shifted = np.fft.fftshift(dft_img)

# Compute the magnitude spectrum (log scale for visualization)
magnitude_spectrum = 20 * np.log(np.abs(dft_shifted))

# Display the original image and its Fourier magnitude spectrum
plt.subplot(121), plt.imshow(img, cmap='gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Fourier Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()
