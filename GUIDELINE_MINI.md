# Mini guideline - Pham Anh Tuan

## Class definitions

| Class | Definition | Distinguishing examples |
| --- | --- | --- |
| `car` | Passenger cars, sedans, hatchbacks, SUVs, taxis, and small pickup trucks. | A road vehicle with a passenger-car body; a small pickup remains `car`. |
| `truck` | Cargo trucks, box trucks, heavy trucks, tractor-trailers, containers, and rescue vehicles built on a truck chassis. | The cargo body or truck chassis is the primary form; do not use `truck` for a small pickup. |
| `bus` | Buses, coaches, and minibuses designed primarily to transport passengers. | A long passenger vehicle with bus layout; ordinary vans and minivans are not `bus`. |
| `van` | Vans and minivans with a box-shaped body for passengers or cargo. | A compact box-shaped vehicle; do not use `van` for a large bus or ordinary car. |

## General rules

- Draw the rectangle around the visible vehicle body, including visible mirrors or cargo extensions when they are part of the vehicle.
- For an occluded vehicle, label the visible object and keep the box within the visible image evidence; do not hallucinate hidden extent.
- For a vehicle cut by the image border, draw the box to the image boundary and label it if enough vehicle evidence remains.
- Label a small or blurry vehicle only when its vehicle shape and class are still identifiable; otherwise leave it for review instead of guessing.

## Ambiguous cases

| Image | Situation | Final decision | Schema reason |
| --- | --- | --- | --- |
| `drive_002` | A small pickup has a short open cargo bed. | `car` | The rubric definition includes pickup trucks in `car` unless the vehicle is a larger cargo-truck form. |
| `drive_035` | A compact passenger vehicle has a tall box-shaped body. | `van` | Body shape and intended passenger/cargo use match the `van` definition, not a regular car. |
| `drive_050` | A long passenger vehicle is partly occluded by another vehicle. | `bus` | The visible length and passenger-bus structure identify it as a bus; the box covers only visible evidence. |
