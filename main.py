import json
import csv


def convert_frame_wise(file_data):
    """convert data into frame wise in json format"""

    frames = dict()
    for tracker in file_data["maker_response"]["video2d"]["data"]["annotations"]:
        for frame_name, frame_data in tracker["frames"].items():
            frame = {
                "_id": frame_data["_id"],
                "label": frame_data["label"],
                "type":frame_data["type"],
                "point_x":frame_data["points"]["p1"]["x"],
                "point_y":frame_data["points"]["p1"]["y"],
                "point_label":frame_data["points"]["p1"]["label"],
                "waering_mask":frame_data["attributes"]["waering_mask"]["value"],
                "wearing_shirt":frame_data["attributes"]["wearing_shirt"]["value"],
                "selfie_validity":frame_data["attributes"]["selfie_validity"]["value"],
                "rider_id":file_data["rider_info"][frame_name]["rider_id"],
                "tracker_id":tracker["_id"]
            }
            if frames.get(frame_name) != None:
                """frame already present """
                frames[frame_name].append(frame)
            else:
                frames[frame_name] = [frame]

    final_output_data = {
        "export_data":{
            "annotations":{
                "frames":frames
            },
            "number of annotations":len(frames)
        }
    }
    # print(json.dumps(final_output_data))
    with open("frame_wise.json",'w') as outfile:
        json.dump(final_output_data,outfile)
    return frames


def convert_into_csv_format(all_frames):
    """convert data into csv format"""

    file_name = "framewise.csv"
    with open(file_name,'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["frame_id","tracking_id","label"])
        for photos in all_frames:
            for frame in all_frames[photos]:
                frame_id = frame["_id"]
                tracking_id = frame["tracker_id"]
                label = frame["label"]
                csvwriter.writerow([frame_id,tracking_id,label])


if __name__ == '__main__':
    file = open("input.json")
    file_data = json.load(file)
    all_frames = convert_frame_wise(file_data)
    convert_into_csv_format(all_frames)
    file.close()