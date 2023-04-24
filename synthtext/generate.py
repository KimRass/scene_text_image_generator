import h5py

db = h5py.File(name="/Users/jongbeomkim/Desktop/workspace/SynthText/data/dset.h5", mode="r")
db.keys()
img = db["image"]["hiking_125.jpg"][:]
depth_map = db["depth"]["hiking_125.jpg"][:].T
seg_map = db["seg"]["hiking_125.jpg"][:]

plt.imshow(seg_map)
plt.show()
# show_image(img)