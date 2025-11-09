from pathlib import Path
from typing import Union
import cv2
import numpy as np

def simple_background_remove(
        input_path: Union[str, Path],
        output_path: Union[str, Path]
) -> Path:
    input_path = Path(input_path)
    output_path = Path(output_path)

    img = cv2.imread(str(input_path), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"Could not read image at {input_path}")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, mask = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    white = np.sum(mask == 255)
    black = np.sum(mask == 0)
    if white > black:
        mask = 255 - mask

    bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = mask

    output_path = output_path.with_suffix('.png')
    cv2.imwrite(str(output_path), bgra)

    return output_path
