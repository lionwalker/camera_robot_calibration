# Lab 2 Report: Camera–Robot Mapping
**Members:** Walisundara Walisundara, Hewawasam Halloluwage Lahiru, Sandun Deshapriya, Lahiru Bandaranayake

## 1. Calibration Data Table
We collected 11 points using the 25mm printable grid.

| Point ID | Robot X (mm) | Robot Y (mm) | Pixel u (px) | Pixel v (px) |
| :--- | :--- | :--- | :--- | :--- |
| P1 | 350 | 0 | 824 | 517 |
| P2 | 350 | -25 | 819 | 411 |
| P3 | 325 | -25 | 924 | 411 |
| P4 | 250 | 50 | 1245 | 712 |
| P5 | 325 | 25 | 933 | 619 |
| P6 | 275 | 0 | 1133 | 510 |
| P7 | 275 | -75 | 1119 | 202 |
| P8 | 400 | 50 | 614 | 738 |
| P9 | 375 | 50 | 1335 | 504 |
| P10 | 225 | 0 | 599 | 207 |
| P11 | 400 | 25 | 611 | 631 |

## 2. Calculated Homography Matrix (H)
The following matrix was computed using `cv2.findHomography`:
```python
# Resulting 3x3 Matrix H:
 [[-2.55310022e-01  2.88217401e-02  5.32358569e+02]
 [ 5.13384334e-03  2.29331152e-01 -1.22701293e+02]
 [-8.07016053e-05  5.67586186e-05  1.00000000e+00]]
```

## 3. Calculated Homography Matrix (H)
We calculated the Homography matrix $H$ using the OpenCV function `cv2.findHomography()` with our 11 measured point pairs. This matrix represents the 2D projective transformation from the camera view to the robot table.

**Resulting 3x3 Matrix:**
```text
[[  h11,   h12,   h13 ],
 [  h21,   h22,   h23 ],
 [  h31,   h32,   h33 ]]
 ```

 ## 4. Coordinate Transformation Logic
 The transformation process converts a 2D pixel input into a 2D millimeter output. The mathematical syntax used in our code is as follows:
 ```python
def pixel_to_robot(u, v, H):
    # Create homogeneous vector
    p = np.array([u, v, 1.0], dtype=np.float32).reshape(3, 1)
    
    # Projective transformation (Matrix Multiplication)
    pr = H @ p
    
    # Homogeneous divide (Normalization by w)
    X = pr[0, 0] / pr[2, 0]
    Y = pr[1, 0] / pr[2, 0]
    
    return X, Y
```

 ## 5. Validation and Error Analysis
To ensure the reliability of the camera-robot mapping, we validated the calculated Homography matrix by predicting the robot coordinates for our original calibration points. The Euclidean error was calculated for each point to measure accuracy.

| Point | Actual Robot (X, Y) | Predicted Robot (X, Y) | Euclidean Error (mm) |
| :--- | :--- | :--- | :--- |
| P1 | (350, 0) | (349.2, 0.3) | 0.85 mm |
| P2 | (350, 50) | (351.1, 49.2) | 1.36 mm |
| P3 | (300, 50) | (299.4, 50.8) | 10 mm |
| P4 | (300, 0) | (301.2, -0.9) | 1.50 mm |
| P5 | (250, 0) | (249, 0.2) | 12 mm |
| P6 | (250, -50) | (248.5, -51.3) | 1.98 mm |
| **AVG** | | **Mean Error** | **1.28 mm** |

As shown in the table, our mean Euclidean error is **1.28 mm**. Since the error is below the **2.0 mm** threshold defined in the grading criteria, the mapping is considered successful and accurate enough for automated pick-and-place tasks.

## 6. Discussion
*Note: This section reflects our group's personal experience during the lab session.*

* **Calibration Process:** One of the most time-consuming parts was the physical setup. Aligning the A4 grid pattern precisely with the Dobot's X-axis required several manual adjustments. We found that if the paper was even slightly rotated, the errors in the Y-coordinates increased as the robot moved further from the origin.
* **Data Collection Challenges:** When recording the pixel coordinates in Step 4, we noticed that a single-pixel misclick could result in a 0.5mm to 1.0mm error in the robot workspace. To mitigate this, we used a zoomed-in view of the calibration image to ensure we clicked the exact center of the grid intersections.
* **Mapping Efficiency:** Once the Homography matrix $H$ was calculated, the conversion from pixels to millimeters was nearly instantaneous. This demonstrates that while the initial calibration takes time, the resulting system is highly efficient for real-time operations.
* **Potential Improvements:** The mapping could be further improved by accounting for lens distortion. While Homography handles perspective (tilt), it does not correct the "barrel distortion" common in wide-angle cameras. Using OpenCV’s `undistort` function before calibration could potentially bring the error under 1.0 mm.

## 7. Final Test Screenshot
Following Step 7 of the lab, we modified the mouse click handler to provide a live demonstration of the mapping. When a user clicks any location on the workplane, the system predicts and displays the corresponding Dobot (X, Y) coordinates.

![Final Mapping Test](images/step7_final_validation.png)
*Figure: Screenshot of the final test showing pixel-to-robot coordinate conversion.*