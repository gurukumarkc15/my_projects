import cv2
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as LA
import scipy.signal as ss
from scipy.ndimage import rotate
import matplotlib
from PIL import Image

def steering_vectors(num_mics,angles,wavelength):
    pi=np.pi
    c=343
    k=2*pi/wavelength
    
    steering_vectors=np.zeros((num_mics,len(angles)),dtype=complex)
    for i,angle in enumerate(angles):
        phase_shifts=k*np.arange(num_mics)*np.sin(angle)
        steering_vectors[:,i]=np.exp(-1j*phase_shifts)
    return steering_vectors

def x(array,angles):
    N=array.shape[0]
    a=steering_vectors(N,angles,1)
    x=a@array
    return x,a

def MUSIC(a,noise_subspace):
    music_spectrum=np.zeros(a.shape[1])
    for i in range(a.shape[1]):
        a1=a[:,i]
        projection=np.dot(noise_subspace.T,a1)
        music_spectrum[i]=1/(np.linalg.norm(projection)**2)
    return music_spectrum

Angles = np.linspace(-np.pi / 2, np.pi / 2, 360)

# Generate synthetic image (replace with your image loading process)
image_path = r"C:\K.C.Gurukarthi2\oil painting.jpg"  # Provide the path to your image
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
rotated_image = rotate(image, angle=90, reshape=False)  # Rotate the image by 45 degrees

image=rotated_image
# img=Image.open(image_path)
# img.show()
plt.figure()
plt.title("Image")
plt.imshow(image)
#plt.imshow(image)
image=cv2.resize(image,(360,360))
plt.figure()
plt.imshow(image)
f_transform=np.fft.fft2(image)
print(image.shape)

#print(height,width,channels)
print(f_transform.shape)
f_transform_shifted=np.fft.fftshift(f_transform)
array=np.abs(f_transform_shifted)
print("shape of array is",array.shape)

x_t,a=x(array,Angles)
print("Shape of x is",x_t.shape)

covariance_matrix=np.cov(x_t)
print("shape of covariance matrix is",covariance_matrix.shape)
N=Angles.shape[0]
eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)
noise_subspace=eigenvectors[:,-N]

music=MUSIC(a,noise_subspace)
plt.figure()


#---------------------------------------------------------------------------------
musicsort=np.sort(music)
plt.plot(Angles,music)
plt.title("MUSIC spectrum")
peaks,_=ss.find_peaks(music,threshold=musicsort[-20])
y=music[peaks]
plt.scatter(Angles[peaks],y, color='r',)
plt.xlabel("Angle")
plt.ylabel("Magnitude")


plt.show()
