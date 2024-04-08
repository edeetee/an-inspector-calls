from yt_dlp import YoutubeDL
import internetarchive as ia
import csv
import glob

csv_file = 'found_footage.csv'
out_dir = 'media'
with open(csv_file) as c:
    reader = csv.reader(c)
    for row in reader:
        print(row)
        n = row[0]
        name = row[1]
        url = row[2]

        out_name = f"{out_dir}/{n}-{name}"

        # skip if file exists
        if glob.glob(f"{out_name}.*"):
            print(f"{out_name} already exists, skipping...")
            continue

        if 'youtube.com' in url:
            with YoutubeDL({"outtmpl": f"{out_name}.%(ext)s"}) as ydl:
                ydl.download([url])

        elif 'archive.org' in url:
            identifier = url.split('/')[-1]
            for file in ia.get_files(identifier):
                if file.format in ["h.254", "h.264", "QuickTime", "MPEG4", "Ogg Video", "Matroska"]:
                    print(f"Downloading {file.name}...")
                    file.download(f"{out_name}.{file.name.split('.')[-1]}")
                    break
                
