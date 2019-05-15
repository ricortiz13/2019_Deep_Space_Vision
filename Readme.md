# Falcon Eye Vision
## Main Algorithm
1. Ensure we have at least 2 contours within the frame
2. Sort remaining contours by size
3. From large to small, authenticate one stripe as target feature
* Keep only top 6 contours
4. During authentication, fingerprint stripe as LEFT or RIGHT
* (`authenticated==True`), **break** progression of list
* (`authenticated==False`), get next contour on list
* After failing to authenticate for all, set `roi = frame`
    * Consider other `roi` resets listed below
5. Use found stripe to locate neighboring stripe
6. Stripe pair is now target, find center of target and compare to center of view
* Return angle delta in degrees to RoboRIO
7. Operate step 1 on ROI

## Better Target Possible: ROI
1. A target has provided data and it is assumed to still be inside the frame
2. Reduce the `roi` to ROI formed by connecting the reflection on the top 2 quadrants of the smallest `roi` achieved during target authentication process and extend it vertically towards the bottom of the frame

## Lost And Found: ROI
1. After a target has been lost, use the location and size of the target's `roi` from the previous frame
2. Grow `roi` by 25% (subject to change with trial and error) in all directions until a new target is found or the max size of the frame has been reched
3. Apply **Main Algorithm** to authenticate and create a new `roi`

## Center Biased Search: ROI
1. Start at frame center and grow outward at rate of 25%
2. Use centroid of largest contour found to expand in that direction
3. Apply **Main Algorithm** to authenticate and create a new `roi`

## Runtime Threads
### Video Server
### Get Frame
### Process Frame
### Data Out
### Data In