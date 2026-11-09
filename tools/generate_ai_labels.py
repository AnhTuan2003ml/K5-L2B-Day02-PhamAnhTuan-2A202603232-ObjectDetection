from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image
from ultralytics import YOLO


TARGET_NAMES = {"car": 0, "truck": 1, "bus": 2, "van": 3}


def tile_positions(length: int, tile_size: int, overlap: float) -> list[int]:
    if length <= tile_size:
        return [0]
    stride = max(1, int(tile_size * (1 - overlap)))
    positions = list(range(0, length - tile_size + 1, stride))
    if positions[-1] != length - tile_size:
        positions.append(length - tile_size)
    return positions


def iou(first: list[float], second: list[float]) -> float:
    left = max(first[0], second[0])
    top = max(first[1], second[1])
    right = min(first[2], second[2])
    bottom = min(first[3], second[3])
    intersection = max(0, right - left) * max(0, bottom - top)
    first_area = max(0, first[2] - first[0]) * max(0, first[3] - first[1])
    second_area = max(0, second[2] - second[0]) * max(0, second[3] - second[1])
    union = first_area + second_area - intersection
    return intersection / union if union else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--images", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--confidence", type=float, default=0.5)
    parser.add_argument("--class-confidence", action="append", default=[])
    parser.add_argument("--iou", type=float, default=0.5)
    parser.add_argument("--imgsz", type=int, default=1024)
    parser.add_argument("--tile-size", type=int, default=0)
    parser.add_argument("--tile-overlap", type=float, default=0.20)
    parser.add_argument("--device", default="0")
    args = parser.parse_args()
    class_confidence = {item.split("=", 1)[0].strip().lower(): float(item.split("=", 1)[1]) for item in args.class_confidence}
    predict_confidence = min([args.confidence, *class_confidence.values()]) if class_confidence else args.confidence

    model = YOLO(str(args.model), task="detect")
    model_names = model.names
    names = model_names if isinstance(model_names, dict) else dict(enumerate(model_names))
    class_map = {class_id: TARGET_NAMES[name.lower()] for class_id, name in names.items() if name.lower() in TARGET_NAMES}
    if not class_map:
        raise SystemExit("Model does not contain car, truck, bus or van classes")

    args.output.mkdir(parents=True, exist_ok=True)
    metadata = {}
    for image_path in sorted(args.images.glob("*")):
        if image_path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        image = Image.open(image_path).convert("RGB")
        width, height = image.size
        tiles = [(image, 0, 0)]
        if args.tile_size and (width > args.tile_size or height > args.tile_size):
            tiles = [
                (image.crop((left, top, left + args.tile_size, top + args.tile_size)), left, top)
                for top in tile_positions(height, args.tile_size, args.tile_overlap)
                for left in tile_positions(width, args.tile_size, args.tile_overlap)
            ]
        detections = []
        scores = []
        for tile, left, top in tiles:
            result = model.predict(
                source=tile,
                imgsz=args.imgsz,
                conf=predict_confidence,
                iou=args.iou,
                device=args.device,
                half=args.device != "cpu",
                max_det=300,
                verbose=False,
            )[0]
            if result.boxes is None:
                continue
            for box, confidence, class_id in zip(
                result.boxes.xyxy.cpu().tolist(),
                result.boxes.conf.cpu().tolist(),
                result.boxes.cls.cpu().tolist(),
            ):
                source_class = int(class_id)
                if source_class not in class_map:
                    continue
                if float(confidence) < class_confidence.get(names[source_class].lower(), args.confidence):
                    continue
                x1, y1, x2, y2 = box
                detections.append((source_class, [x1 + left, y1 + top, x2 + left, y2 + top], float(confidence)))
        detections.sort(key=lambda item: item[2], reverse=True)
        kept = []
        for detection in detections:
            if any(detection[0] == previous[0] and iou(detection[1], previous[1]) >= 0.65 for previous in kept):
                continue
            kept.append(detection)
        rows = []
        for source_class, box, confidence in kept:
            x1, y1, x2, y2 = box
            x1, x2 = max(0.0, min(x1, width)), max(0.0, min(x2, width))
            y1, y2 = max(0.0, min(y1, height)), max(0.0, min(y2, height))
            box_width, box_height = x2 - x1, y2 - y1
            if box_width <= 0 or box_height <= 0:
                continue
            rows.append(
                f"{class_map[source_class]} {(x1 + x2) / 2 / width:.6f} {(y1 + y2) / 2 / height:.6f} "
                f"{box_width / width:.6f} {box_height / height:.6f}"
            )
            scores.append(confidence)
        (args.output / f"{image_path.stem}.txt").write_text("\n".join(rows) + ("\n" if rows else ""), encoding="utf-8")
        metadata[image_path.stem] = {"boxes": len(rows), "confidences": scores}
    (args.output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"images": len(metadata), "boxes": sum(item["boxes"] for item in metadata.values())}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
