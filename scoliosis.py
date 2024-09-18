"""
version: v1.1.0
Author(s): Andres Marquez
Source: https://github.com/Andres-Dead/kinect-project/tree/main
Contact: amarquez9801@gmail.com
All rights reserved
"""

import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Scale  conversion from pixels to centimeters
PIXELS_PER_CM = 30  # Example: 30 pixels = 1 cm

def calculate_angle(p1, p2, p3):
    """Calculate angle between three points."""
    a = np.array([p1[0] - p2[0], p1[1] - p2[1]])
    b = np.array([p3[0] - p2[0], p3[1] - p2[1]])
    angle = np.arccos(np.clip(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)), -1.0, 1.0))
    return np.degrees(angle)

def get_landmark_coordinates(landmarks, height, width):
    """Convert frame to pixel coordinates."""
    return {
        'shoulder_left': (int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * width),
                          int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * height)),
        'shoulder_right': (int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * width),
                           int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * height)),
        'hip_left': (int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * width),
                     int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * height)),
        'hip_right': (int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x * width),
                      int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y * height)),
        'ear_left': (int(landmarks[mp_pose.PoseLandmark.LEFT_EAR].x * width),
                     int(landmarks[mp_pose.PoseLandmark.LEFT_EAR].y * height)),
        'ear_right': (int(landmarks[mp_pose.PoseLandmark.RIGHT_EAR].x * width),
                      int(landmarks[mp_pose.PoseLandmark.RIGHT_EAR].y * height)),
        'ankle_left': (int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x * width),
                       int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y * height)),
        'ankle_right': (int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x * width),
                        int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y * height)),
    }

def draw_landmarks(frame, landmarks):
    """Draw landmarks on the frame."""
    colors = {
        'shoulder': (0, 255, 0),
        'ear': (255, 0, 0),
        'ankle': (0, 0, 255),
    }
    for name, (x, y) in landmarks.items():
        color = colors['shoulder'] if 'shoulder' in name or 'hip' in name else colors['ear'] if 'ear' in name else colors['ankle']
        cv2.circle(frame, (x, y), 5, color, -1)

def draw_labels(frame, landmarks):
    """Label each point with letters A to F."""
    labels = {
        'A': landmarks['shoulder_left'],
        'B': landmarks['shoulder_right'],
        'C': (landmarks['shoulder_left'][0], (landmarks['hip_left'][1] + landmarks['shoulder_left'][1]) // 2),
        'D': (landmarks['shoulder_right'][0], (landmarks['hip_right'][1] + landmarks['shoulder_right'][1]) // 2),
        'E': landmarks['hip_left'],
        'F': landmarks['hip_right'],
    }
    for label, (x, y) in labels.items():
        cv2.putText(frame, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

def main():
    cap = cv2.VideoCapture(0)
    img_counter = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame and get pose templates
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            height, width, _ = frame.shape
            landmarks = get_landmark_coordinates(results.pose_landmarks.landmark, height, width)

            # Draw landmarks on frame
            draw_landmarks(frame, landmarks)
            draw_labels(frame, landmarks)

            # Calculate midpoints
            mid_spine_x = (landmarks['shoulder_left'][0] + landmarks['shoulder_right'][0]) // 2
            mid_waist_y = (landmarks['hip_left'][1] + landmarks['hip_right'][1]) // 2
            mid_line_y = (landmarks['shoulder_left'][1] + mid_waist_y) // 2

            # Draw lines and calculate angles
            if abs(landmarks['shoulder_left'][0] - landmarks['shoulder_right'][0]) < 50:
                draw_sideways_lines(frame, landmarks)
                display_angles(frame, landmarks, mid_waist_y)

            if shoulder_is_visible(landmarks):
                draw_back_view_lines(frame, landmarks, mid_spine_x)

            # Draw connecting lines
            draw_connecting_lines(frame, landmarks, mid_line_y)

            # Display distances
            display_distances(frame, landmarks, mid_line_y)

        # Show the frame and turn on camera
        cv2.imshow('Scoliosis Level Detection', frame)

        # Capture images based on key presses
        key = cv2.waitKey(5) & 0xFF
        if key in {ord('1'), ord('2'), ord('3')}:
            cv2.imwrite(f'{["sideways", "back", "back_crouch"][key - ord("1")]}_view_{img_counter}.png', frame)
            img_counter += 1
        elif key == 27:  # Press 'ESC' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

def draw_sideways_lines(frame, landmarks):
    """Draw lines for sideways view."""
    cv2.line(frame, landmarks['ear_left'], landmarks['hip_left'], (255, 200, 200), 2)
    cv2.line(frame, landmarks['hip_left'], landmarks['ankle_left'], (255, 200, 200), 2)
    cv2.line(frame, landmarks['ear_right'], landmarks['hip_right'], (255, 200, 200), 2)
    cv2.line(frame, landmarks['hip_right'], landmarks['ankle_right'], (255, 200, 200), 2)

def display_angles(frame, landmarks, mid_waist_y):
    """Display angles based on landmarks."""
    angle_left = calculate_angle(landmarks['ear_left'], landmarks['hip_left'], landmarks['ankle_left'])
    angle_right = calculate_angle(landmarks['ear_right'], landmarks['hip_right'], landmarks['ankle_right'])

    cv2.putText(frame, f"Left Angle: {angle_left:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Right Angle: {angle_right:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

def shoulder_is_visible(landmarks):
    """Check if shoulders are roughly aligned."""
    return (landmarks['shoulder_left'][1] < landmarks['shoulder_right'][1] + 50 and
            landmarks['shoulder_left'][1] > landmarks['shoulder_right'][1] - 50)

def draw_back_view_lines(frame, landmarks, mid_spine_x):
    """Draw lines for back view."""
    cv2.line(frame, landmarks['shoulder_left'], landmarks['shoulder_right'], (0, 255, 255), 2)
    cv2.line(frame, landmarks['hip_left'], landmarks['hip_right'], (0, 255, 255), 2)

    shoulder_angle = calculate_angle(landmarks['shoulder_left'], landmarks['shoulder_right'], (mid_spine_x, landmarks['shoulder_left'][1]))
    cv2.putText(frame, f"Shoulder Inclination: {shoulder_angle:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    hip_angle = calculate_angle(landmarks['hip_left'], landmarks['hip_right'], (mid_spine_x, landmarks['hip_left'][1]))
    cv2.putText(frame, f"Hip Inclination: {hip_angle:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

def draw_connecting_lines(frame, landmarks, mid_line_y):
    """Connect points A to C and B to D, and draw the middle line."""
    cv2.line(frame, landmarks['shoulder_left'], (landmarks['shoulder_left'][0], mid_line_y), (255, 0, 0), 2)  # A to C
    cv2.line(frame, landmarks['shoulder_right'], (landmarks['shoulder_right'][0], mid_line_y), (255, 0, 0), 2)  # B to D
    cv2.line(frame, (landmarks['shoulder_left'][0], mid_line_y), landmarks['hip_left'], (0, 255, 0), 2)  # C to E
    cv2.line(frame, (landmarks['shoulder_right'][0], mid_line_y), landmarks['hip_right'], (0, 255, 0), 2)  # D to F
    cv2.line(frame, (landmarks['shoulder_left'][0], mid_line_y), (landmarks['shoulder_right'][0], mid_line_y), (0, 255, 255), 2)  # Middle Line

def display_distances(frame, landmarks, mid_line_y):
    """Calculate and display distances between points."""
    distances = {
        'A to C': np.linalg.norm(np.array([landmarks['shoulder_left'][0], landmarks['shoulder_left'][1]]) - np.array([landmarks['shoulder_left'][0], mid_line_y])) / PIXELS_PER_CM,
        'B to D': np.linalg.norm(np.array([landmarks['shoulder_right'][0], landmarks['shoulder_right'][1]]) - np.array([landmarks['shoulder_right'][0], mid_line_y])) / PIXELS_PER_CM,
        'C to E': np.linalg.norm(np.array([landmarks['shoulder_left'][0], mid_line_y]) - np.array(landmarks['hip_left'])) / PIXELS_PER_CM,
        'D to F': np.linalg.norm(np.array([landmarks['shoulder_right'][0], mid_line_y]) - np.array(landmarks['hip_right'])) / PIXELS_PER_CM,
    }

    # Display distances on CM
    cv2.putText(frame, f"A to C: {distances['A to C']:.2f} cm", (landmarks['shoulder_left'][0] + 100, mid_line_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    cv2.putText(frame, f"B to D: {distances['B to D']:.2f} cm", (landmarks['shoulder_right'][0] - 500, mid_line_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    cv2.putText(frame, f"C to E: {distances['C to E']:.2f} cm", (landmarks['hip_left'][0] + 100, landmarks['hip_left'][1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    cv2.putText(frame, f"D to F: {distances['D to F']:.2f} cm", (landmarks['hip_right'][0] - 500, landmarks['hip_right'][1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

if __name__ == "__main__":
    main()
