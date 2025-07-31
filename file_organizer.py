import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#---Configuration---

#Define Documents folder path
downloads = "C:/Users/Lenovo/Downloads"
#File types to organize
file_types = {
	"Images" : [".jpg", ".png", ".gif", ".jpeg"],
	"PDFs" : [".pdf"],
	"Documents" : [".docx", ".txt", "xlsx", ".pptx", ".ppt", ".xls"],
	"Videos" : [".mp4", ".mov"],
	"Music" : [".mp3", ".wav"],
	"Datasets Excel" : [".csv"],
	"Archieves" : [".zip"],
	"Packet Tracer Act" : [".pka"]
}

#---Core Organizer Function---
def organize_files():
	#Create folders if missing
	for folder in file_types.keys():
		os.makedirs(os.path.join(downloads, folder), exist_ok = True)

	#Process files
	for file in os.listdir(downloads):
		file_path = os.path.join(downloads, file)

		if os.path.isdir(file_path) or file.startswith('.'):
			continue

		#move files
		for folder, extensions in file_types.items():
			if any(file.lower().endswith(ext) for ext in extensions):
				shutil.move(file_path, os.path.join(downloads, folder, file))
				print(f"📂 Moved: {file} → {folder}/")
				break

#---Watchdog Handler---
class DownloadHandler(FileSystemEventHandler):
	def on_modified(self,event):
		#Triggered when Downloads folder is modified
		organize_files()

#---Main Execution---
if __name__ == "__main__":
	print(f"🚀 Starting real-time organizer for: {downloads}")

	#Initial Organization
	organize_files()

	#Set up watchdog observer
	event_handler = DownloadHandler()
	observer = Observer()
	observer.schedule(event_handler, downloads, recursive=False)
	observer.start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer