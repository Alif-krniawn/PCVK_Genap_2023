import cv2
import tkinter as tk
from PIL import Image, ImageTk

# Fungsi untuk mengaburkan wajah
def blur_faces(image, faces):
    for (x, y, w, h) in faces:
        # Mengambil bagian wajah
        face = image[y:y+h, x:x+w]
        
        # Mengaburkan wajah
        blurred_face = cv2.GaussianBlur(face, (99, 99), 30)
        
        # Menempatkan wajah yang diaburkan kembali ke gambar asli
        image[y:y+h, x:x+w] = blurred_face
    
    return image

# Inisialisasi webcam
cap = cv2.VideoCapture(0)

# Memuat classifier wajah
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Membuat jendela GUI menggunakan Tkinter
window = tk.Tk()
window.title("Face Blurring Camera")

# Fungsi untuk menangkap gambar dari webcam
def capture_image():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    blurred_frame = blur_faces(frame, faces)
    cv2.imwrite("captured_image.jpg", blurred_frame)
    image = Image.fromarray(cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2RGB))
    image.thumbnail((400, 400))
    photo = ImageTk.PhotoImage(image)
    captured_label.configure(image=photo)
    captured_label.image = photo

# Tombol untuk menangkap gambar
capture_button = tk.Button(window, text="Capture Image", command=capture_image)
capture_button.pack(pady=10)

# Label untuk menampilkan gambar yang ditangkap
captured_label = tk.Label(window)
captured_label.pack()

# Fungsi untuk update tampilan GUI
def update_frame():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    blurred_frame = blur_faces(frame, faces)
    image = Image.fromarray(cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2RGB))
    image.thumbnail((800, 600))
    photo = ImageTk.PhotoImage(image)
    video_label.configure(image=photo)
    video_label.image = photo
    window.after(10, update_frame)

# Label untuk menampilkan video dari webcam
video_label = tk.Label(window)
video_label.pack()

# Memulai update tampilan GUI
update_frame()

# Memulai GUI
window.mainloop()

# Membersihkan dan menutup program
cap.release()
cv2.destroyAllWindows()