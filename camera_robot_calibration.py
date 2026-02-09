import cv2
import numpy as np

# --- SECTION 1: CALIBRATION DATA ---
img_pts = np.array([
    [824, 517],
    [819, 411],
    [924, 411],
    [1245, 712],
    [933, 619],
    [1133, 510],
    [811, 203],
    [1119, 202],
    [614, 738],
    [611, 630],
    [722, 733],
    [599, 207],
], dtype=np.float32)

robot_pts = np.array([
    [350, 0],
    [350, -25],
    [325, -25],
    [250, 50],
    [325, 25],
    [275, 0],
    [350, -75],
    [275, -75],
    [400, 50],
    [400, 25],
    [375, 50],
    [400, -75],
], dtype=np.float32)

# --- SECTION 2: HOMOGRAPHY CALCULATION ---
H, mask = cv2.findHomography(img_pts, robot_pts, method=cv2.RANSAC)

# --- SECTION 3: MAPPING FUNCTION ---


def pixel_to_robot(u, v, H):
    # Input: u, v as floats, H as 3x3 homography
    p = np.array([u, v, 1.0], dtype=np.float32).reshape(3, 1)
    pr = H @ p
    pr = pr / pr[2, 0]  # divide by last coordinate to normalize
    X = pr[0, 0]
    Y = pr[1, 0]

    return X, Y


# --- SECTION 4: VALIDATION LOOP ---
print(f"{'Point':<6} | {'Actual (X, Y)':<18} | {'Predicted (X, Y)':<22} | {'Error (mm)':<10}")
print("-" * 70)

errors = []
for i in range(len(img_pts)):
    u, v = img_pts[i]
    x_act, y_act = robot_pts[i]
    x_pred, y_pred = pixel_to_robot(u, v, H)

    # Calculate Euclidean Error: sqrt((dx^2) + (dy^2))
    err = np.sqrt((x_act - x_pred)**2 + (y_act - y_pred)**2)
    errors.append(err)

    print(f"P{i+1:<4} | ({x_act:>5.1f}, {y_act:>5.1f})   | ({x_pred:>7.2f}, {y_pred:>7.2f})   | {err:>8.3f}")

print("-" * 70)
print(f"Average Mean Error: {np.mean(errors):.2f} mm")
print(f"Maximum Error:      {np.max(errors):.2f} mm")

# --- SECTION 5: INTERACTIVE TEST (Step 7) ---
img_display = cv2.imread('images/calib_image_with_tiles.jpg')


def mouse_callback(event, u, v, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Convert the click location to robot coordinates
        X_rob, Y_rob = pixel_to_robot(u, v, H)

        # Log to console
        print(
            f"Clicked Pixel: ({u}, {v}) -> Robot Coordinate: ({X_rob:.1f}, {Y_rob:.1f}) mm")

        # Visual feedback on the image
        cv2.circle(img_display, (u, v), 6, (0, 0, 255), -1)
        coord_text = f"X:{X_rob:.1f}, Y:{Y_rob:.1f}"
        cv2.putText(img_display, coord_text, (u + 15, v - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        cv2.imshow('Step 7: Final Test', img_display)


cv2.namedWindow('Step 7: Final Test')
cv2.setMouseCallback('Step 7: Final Test', mouse_callback)

print("--- Lab 2: Final Test ---")
print("Click on any object in the window to see its Robot Coordinates.")
print("Press 'ESC' to close the window and finish.")

while True:
    cv2.imshow('Step 7: Final Test', img_display)
    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC key
        # SAVE THE IMAGE before closing
        filename = "images/step7_final_validation.png"
        cv2.imwrite(filename, img_display)
        print(f"Image successfully saved as {filename}")
        break

cv2.destroyAllWindows()
