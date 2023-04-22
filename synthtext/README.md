# Paper Reading
- [Synthetic Data for Text Localisation in Natural Images](https://arxiv.org/pdf/1604.06646v1.pdf)
## Introduction
- First, we propose a new method for generating synthetic images of text that naturally blends text in existing natural scenes, using off-the-shelf deep learning and segmentation techniques to align text to the geometry of a background image and respect scene boundaries.
- ***We also demonstrate the importance of verisimilitude in the dataset by showing that if the detector is trained on images with words inserted synthetically that do not take account of the scene layout, then the detection performance is substantially inferior.***
- Our synthetic engine (1) produces realistic scene-text images so that the trained models can generalize to real (non-synthetic) images, (2) is fully automated and, is (3) fast, which enables the generation of large quantities of data without supervision.
- Process
    - Figure 3
        - <img src="https://user-images.githubusercontent.com/67457712/233758260-b248a597-a84e-41d6-9161-0b9c6f349e5d.png" width="900">
        - (Top): (1) RGB input image with no text instance. (2) Predicted dense depth map (darker regions are closer). (3) color and texture gPb-UCM segments. (4) Filtered regions: regions suitable for text are colored randomly; those unsuitable retain their original image pixels.
        - (Bottom): Four synthetic scene-text images with axis-aligned bounding-box annotations at the word level.
        - The text generation pipeline can be summarized as follows. After acquiring suitable text and image samples, the image is segmented into contiguous regions based on local color and texture cues [2], and a dense pixel-wise depth map is obtained using the CNN of [30] Then, for each contiguous region a local surface normal is estimated.
        - Next, a color for text and, optionally, for its outline is chosen based on the region’s color. Finally, a text sample is rendered using a randomly selected font and transformed according to the local surface orientation; the text is blended into the scene using Poisson image editing [35]. Our engine takes about half a second to generate a new scene-text image.
- Text and Image Sources
    - The synthetic text generation process starts by sampling some text and a background image. The text is extracted from the Newsgroup20 dataset in three ways — words, lines (up to 3 lines) and paragraphs (up to 7 lines). Words are defined as tokens separated by whitespace characters, lines are delimited by the newline character.
    - To favour variety, 8,000 background images are extracted from Google Image Search through queries related to different objects/scenes and indoor/outdoor and natural/artificial locales. ***To guarantee that all text occurrences are fully annotated, these images must not contain text of their own. Hence, keywords which would recall a large amount of text in the images (e.g. "street-sign", "menu" etc.) are avoided; images containing text are discarded through manual inspection.***
- Segmentation and Geometry Estimation
    - ***In real images, text tends to be contained in well defined regions (e.g. a sign). We approximate this constraint by requiring text to be contained in regions characterized by a uniform color and texture. This also prevents text from crossing strong image discontinuities, which is unlikely to occur in practice. Regions are obtained by thresholding the gPb-UCM contour hierarchies [2] at*** $0.11$ ***using the efficient graph-cut implementation of [3].
    - ***In natural images, text tends to be painted on top of surfaces (e.g. a sign or a cup). In order to approximate a similar effect in our synthetic data, the text is perspectively transformed according to local surface normals. The normals are estimated automatically by first predicting a dense depth map using the CNN of [30] for the regions segmented above, and then fitting a planar facet to it using RANSAC.***
    - Text is aligned to the estimated region orientations as follows: first, the image region contour is warped to a frontal-parallel view using the estimated plane normal; then, a rectangle is fitted to the fronto-parallel region; finally, the text is aligned to the larger side ("width") of this rectangle.
    - ***When placing multiple instances of text in the same region, text masks are checked for collision against each other to avoid placing them on top of each other.***
    - ***Not all segmentation regions are suitable for text placement — regions should not be too small, have an extreme aspect ratio, or have surface normal orthogonal to the viewing direction; all such regions are filtered in this stage. Further, regions with too much texture are also filtered, where the degree of texture is measured by the strength of third derivatives in the RGB image.***
    - Figure 4: Local color/texture sensitive placement
        - <img src="https://user-images.githubusercontent.com/67457712/233759012-b741d382-ef90-4c30-9bb4-91c6d8d4728f.png" width="500">
        - (Left): Example image from the Synthetic text dataset. Notice that the text is restricted within the boundaries of the step in the street.
        - (Right): For comparison, the placement of text in this image does not respect the local region cues.
- Text Rendering and Image Composition
    - Once the location and orientation of text has been decided, text is assigned a color. The color palette for text is learned from cropped word images in the IIIT5K word dataset [32]. ***Pixels in each cropped word images are partitioned into two sets using K-means, resulting in a color pair, with one color approximating the foreground (text) color and the other the background. When rendering new text, the color pair whose background color matches the target image region the best (using L2-norm in the CIELAB color space) is selected, and the corresponding foreground color is used to render the text. About 20% of the text instances are randomly chosen to have a border. The border color is chosen to be either the same as foreground color with its value channel increased or decreased, or is chosen to be the mean of the foreground and background colors. To maintain the illumination gradient in the synthetic text image, we blend the text on to the base image using Poisson image editing [35], with the guidance field defined as in their equation (12). We solve this efficiently using the implementation provided by Raskar1.***
## Discussions
- An alternative to using a CNN to estimate depth, which is an error prone process, is to use a dataset of RGBD images. We prefer to estimate an imperfect depth map instead because: (1) it allows essentially any scene type background image to be used, instead of only the ones for which RGBD data are available, and (2) because publicly available RGBD datasets such as NYUDv2, B3DO, Sintel, and Make3D have several limitations in our context: small size (1,500 images in NYUDv21, 400 frames in Make3D, and a small number of videos in B3DO and Sintel), low-resolution and motion blur, restriction to indoor images (in NYUDv2 and B3DO), and limited variability in the images for video-based datasets (B3DO and Sintel).
## References
- [2] [Contour Detection and Hierarchical Image Segmentation](https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/papers/amfm_pami2010.pdf)
- [3] [Multiscale Combinatorial Grouping](https://openaccess.thecvf.com/content_cvpr_2014/papers/Arbelaez_Multiscale_Combinatorial_Grouping_2014_CVPR_paper.pdf)
- [30] [Deep Convolutional Neural Fields for Depth Estimation from a Single Image](https://arxiv.org/pdf/1411.6387.pdf)
- [32] [Scene Text Recognition using Higher Order Language Priors](https://www.di.ens.fr/willow/pdfscurrent/mishra12a.pdf)
- [35] [Poisson Image Editing](https://www.cs.jhu.edu/~misha/Fall07/Papers/Perez03.pdf)