import cv2


def enhance_frame(frame, scale=2, method='cubic'):
    inter_methods = {
        'cubic': cv2.INTER_CUBIC,
        'linear': cv2.INTER_LINEAR,
        'lanczos': cv2.INTER_LANCZOS4
    }
    inter = inter_methods.get(method.lower(), cv2.INTER_CUBIC)

    new_w = int(frame.shape[1] * scale)
    new_h = int(frame.shape[0] * scale)
    return cv2.resize(frame, (new_w, new_h), interpolation=inter)


def enhance_video(input_path, output_path, scale=2, method='cubic'):
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale)
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
    while True:
        ret, frame = cap.read()
        if not ret: break
        enriched_frame = enhance_frame(frame, scale, method)
        out.write(enriched_frame)

    cap.release()
    out.release()
    return output_path
