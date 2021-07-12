# **Finding Lane Lines on the Road** 

## Writeup

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

So with the helper functions provided in the notebook I was able to build the first straight forward version of the pipeline by using the standard hough transform values and canny edges parameter tunning. I used the region of interest to start on the x axis on the 100 pixel because it was detecting a few outliers at first.

After modifying the notebook to test accross the different test images and the two videos and not clog the notebook, I moved the helpers on to its own `helpers.py` and the pipeline to its `pipeline.py` file. This way the notebook is easier to got through.

Enhancing the `draw_lines()` function was the tricky part, after researching different approaches and asking for help, I approached the brute-force approach and the first thing I did was to detect the right and left lanes based on the sign of the slope and put them in a list. The slope is detected by using the `polyfit` function and we also persist the min value of the y axis found on each line. I asked a question on how to do the "extrapolation" on the knowledge base and the `np.mean()` function was suggested by one of the mentors.

So the idea was to get the line for each of the lane by getting the average values of x, y, m and b and plot each of those "average" lanes, it worked in the images and the first video, unfortunately I stumbled upon an annoying `NaaN is not a number` error in the second video. After some troubleshooting, somehow some images don't detect valid line values. I added a statement to calculate the mean values only if there were valid slope values gotten from the lines and this seems to fix the issue.


### 2. Identify potential shortcomings with your current pipeline


A lot.

- The draw_lines function implements an nested loop to traverse each point on each line, this may not be time effective so this may lead to performance degradation.

- It clearly only detects straight lines and when the video is a bit bumpy it fails to detect valid lines.

- I used almost the same parameters as the video lessons and quizzes tought me so thsi may very well be missing better paramters.


### 3. Suggest possible improvements to your pipeline

A lot

- Unit and integration testing to make a robust lifecycle and code quality pipeline
- Hough parameters are considered static here, my guess would be if there was a mechanism to detect the right hough parameters for each frame it would be nice.
- Again, the region of interest vertices is considered static, this may very well fail to detect only the lanes if the video starts to move and the optial ROI changes. A mechanism to detect waht are the optimal vertices for the ROI would be great, IMO.
- I would explore or research for a better way to traverse over each point of each detected line as it the time complexity for this brute force approach may very well be not performant in production.
