import csv
import json

def csv_to_geojson(csv_file, geojson_file):
    features = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 緯度・経度が空でないことを確認
            if row['latitude'] and row['longitude']:
                try:
                    feature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [float(row['longitude']), float(row['latitude'])]
                        },
                        "properties": {k: v for k, v in row.items() if k not in ['latitude', 'longitude']}
                    }
                    features.append(feature)
                except ValueError:
                    # 緯度・経度が数値に変換できない場合はスキップ
                    print(f"Warning: Skipping row with invalid coordinates: {row.get('stream_title', 'Unknown')}")

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(geojson_file, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print(f"Converted {len(features)} features to {geojson_file}")

if __name__ == "__main__":
    csv_to_geojson('livecamera-jp.csv', 'livecamera-jp.geojson')
