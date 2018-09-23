import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pickle
import cv2
import utils
import glob
import os
from scipy.ndimage.measurements import label
from moviepy.editor import VideoFileClip


dist_pickle = pickle.load(open("vehical_dist.p", "rb"))
svc = dist_pickle["clf"]
X_scaler = dist_pickle["scaler"]
orient = dist_pickle["orient"]
pix_per_cell = dist_pickle["pix_per_cell"]
cell_per_block = dist_pickle["cell_per_block"]
spatial_size = dist_pickle["spatial_size"]
hist_bins = dist_pickle["hist_bins"]




# Define a single function that can extract features using hog sub-sampling and make predictions
def find_cars(img, ystart, ystop, scale, cspace, hog_channel, svc, X_scaler, orient,
              pix_per_cell, cell_per_block, spatial_size, hist_bins, show_all_rectangles=False):
    # array of rectangles where cars were detected
    windows = []

    img = img.astype(np.float32) / 255

    img_tosearch = img[ystart:ystop, :, :]

    # apply color conversion if other than 'RGB'
    if cspace != 'RGB':
        if cspace == 'HSV':
            ctrans_tosearch = cv2.cvtColor(img_tosearch, cv2.COLOR_RGB2HSV)
        elif cspace == 'LUV':
            ctrans_tosearch = cv2.cvtColor(img_tosearch, cv2.COLOR_RGB2LUV)
        elif cspace == 'HLS':
            ctrans_tosearch = cv2.cvtColor(img_tosearch, cv2.COLOR_RGB2HLS)
        elif cspace == 'YUV':
            ctrans_tosearch = cv2.cvtColor(img_tosearch, cv2.COLOR_RGB2YUV)
        elif cspace == 'YCrCb':
            ctrans_tosearch = cv2.cvtColor(img_tosearch, cv2.COLOR_RGB2YCrCb)
    else:
        ctrans_tosearch = np.copy(img)

    # rescale image if other than 1.0 scale
    if scale != 1:
        imshape = ctrans_tosearch.shape
        ctrans_tosearch = cv2.resize(ctrans_tosearch, (np.int(imshape[1] / scale), np.int(imshape[0] / scale)))

    # select colorspace channel for HOG
    if hog_channel == 'ALL':
        ch1 = ctrans_tosearch[:, :, 0]
        ch2 = ctrans_tosearch[:, :, 1]
        ch3 = ctrans_tosearch[:, :, 2]
    else:
        ch1 = ctrans_tosearch[:, :, hog_channel]

    # Define blocks and steps as above
    nxblocks = (ch1.shape[1] // pix_per_cell) + 1  # -1
    nyblocks = (ch1.shape[0] // pix_per_cell) + 1  # -1
    nfeat_per_block = orient * cell_per_block ** 2
    # 64 was the orginal sampling rate, with 8 cells and 8 pix per cell
    window = 64
    nblocks_per_window = (window // pix_per_cell) - 1
    cells_per_step = 2  # Instead of overlap, define how many cells to step
    nxsteps = (nxblocks - nblocks_per_window) // cells_per_step
    nysteps = (nyblocks - nblocks_per_window) // cells_per_step

    # Compute individual channel HOG features for the entire image
    hog1 = utils.get_hog_features(ch1, orient, pix_per_cell, cell_per_block, feature_vec=False)
    if hog_channel == 'ALL':
        hog2 = utils.get_hog_features(ch2, orient, pix_per_cell, cell_per_block, feature_vec=False)
        hog3 = utils.get_hog_features(ch3, orient, pix_per_cell, cell_per_block, feature_vec=False)

    for xb in range(nxsteps):
        for yb in range(nysteps):
            ypos = yb * cells_per_step
            xpos = xb * cells_per_step
            # Extract HOG for this patch
            hog_feat1 = hog1[ypos:ypos + nblocks_per_window, xpos:xpos + nblocks_per_window].ravel()
            if hog_channel == 'ALL':
                hog_feat2 = hog2[ypos:ypos + nblocks_per_window, xpos:xpos + nblocks_per_window].ravel()
                hog_feat3 = hog3[ypos:ypos + nblocks_per_window, xpos:xpos + nblocks_per_window].ravel()
                hog_features = np.hstack((hog_feat1, hog_feat2, hog_feat3))
            else:
                hog_features = hog_feat1

            xleft = xpos * pix_per_cell
            ytop = ypos * pix_per_cell



            test_prediction = svc.predict(hog_features.reshape(1,-1))

            if test_prediction == 1 or show_all_rectangles:
                xbox_left = np.int(xleft * scale)
                ytop_draw = np.int(ytop * scale)
                win_draw = np.int(window * scale)
                windows.append(
                    ((xbox_left, ytop_draw + ystart), (xbox_left + win_draw, ytop_draw + win_draw + ystart)))

    return windows

def search_car(img,framecount):
    draw_img = np.copy(img)

    windows = []

    colorspace = 'YUV'  # Can be RGB, HSV, LUV, HLS, YUV, YCrCb
    orient = 11
    pix_per_cell = 16
    cell_per_block = 2
    hog_channel = 'ALL'  # Can be 0, 1, 2, or "ALL"

    ystart = 400
    ystop = 464
    scale = 1.0
    windows+=(find_cars(img, ystart, ystop, scale, colorspace, hog_channel, svc, None,
                                orient, pix_per_cell, cell_per_block, None, None))
    ystart = 416
    ystop = 480
    scale = 1.0
    windows+=(find_cars(img, ystart, ystop, scale, colorspace, hog_channel, svc, None,
                                orient, pix_per_cell, cell_per_block, None, None))
    ystart = 400
    ystop = 496
    scale = 1.5
    windows+=(find_cars(img, ystart, ystop, scale, colorspace, hog_channel, svc, None,
                                orient, pix_per_cell, cell_per_block, None, None))
    ystart = 432
    ystop = 528
    scale = 1.5
    windows += (find_cars(img, ystart, ystop, scale, colorspace, hog_channel, svc, None,
                          orient, pix_per_cell, cell_per_block, None, None))
    ystart = 400
    ystop = 528
    scale = 2.0
    windows += (find_cars(img, ystart, ystop, scale, colorspace, hog_channel, svc, None,
                          orient, pix_per_cell, cell_per_block, None, None))
    ystart = 432
    ystop = 560
    scale = 2.0
    windows += (find_cars(img, ystart, ystop, scale, colorspace, hog_channel, svc, None,
                          orient, pix_per_cell, cell_per_block, None, None))
    ystart = 400
    ystop = 596
    scale = 3.5
    windows += (find_cars(img, ystart, ystop, scale, colorspace, hog_channel, svc, None,
                          orient, pix_per_cell, cell_per_block, None, None))
    ystart = 464
    ystop = 660
    scale = 3.5
    windows += (find_cars(img, ystart, ystop, scale, colorspace, hog_channel, svc, None,
                          orient, pix_per_cell, cell_per_block, None, None))
    
#    window_list = utils.slide_window(img)

    
    heat_map = np.zeros(img.shape[:2])
    heat_map = utils.add_heat(heat_map,windows)
    heat_map_thresholded = utils.apply_threshold(heat_map,1)
    labels = label(heat_map_thresholded)
    i=0
    VehicalPath="./capture"
    if not os.path.exists(VehicalPath):
        os.makedirs(VehicalPath)
    draw_img,bboxlist= utils.draw_labeled_bboxes(draw_img,labels)
    for bbox in bboxlist:
        x1,y1=bbox[0]
        x2,y2=bbox[1]
        i=i+1
        if(x2-x1>96) and (y2-y1)>96:
            cv2.imwrite("./capture/Vehical{}_{}.jpg".format(framecount, i), draw_img[x1:x2, y1:y2])
    return VehicalPath
'''

ystart = 400
ystop = 656
scale = 1.5

test_imgs=[]
out_imgs = []
img_paths = glob.glob('test_images/*.jpg')
plt.figure(figsize=(20,68))
for path in img_paths:
   img = mpimg.imread(path)
   print(path)
   out_img = search_car(img)
   test_imgs.append(img)
   out_imgs.append(out_img)

plt.figure(figsize=(20,68))
for i in range(len(test_imgs)):

   plt.subplot(2*len(test_imgs),2,2*i+1)
   plt.imshow(test_imgs[i])

   plt.subplot(2*len(test_imgs),2,2*i+2)
   plt.imshow(out_imgs[i])
   cv2.waitKey()
'''
# #uncomment to run the pipeline on the video
# project_outpath = 'vedio_out/project_video_out.mp4'
# project_video_clip = VideoFileClip("project_video.mp4")
#project_video_out_clip = project_video_clip.fl_image(search_car)
#project_video_out_clip.write_videofile(project_outpath, audio=False)
