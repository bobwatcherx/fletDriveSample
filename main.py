from flet import *
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

gauth = GoogleAuth()

# NOW LOAD IF YOU HAVE LOGIN IN THIS APP 
# THEN LOAD FILE
gauth.LoadCredentialsFile("mycreds.txt")

# IF FOUND LOGIN IN MYCREDS.TXT FILE THEN YOU MUST LOGIN
if gauth.credentials is None:
	gauth.GetFlow()
	gauth.flow.params.update({"access_type":"offline"})
	gauth.flow.params.update({"approval_prompt":"force"})	

	gauth.LocalWebserverAuth()

# IF YOU LOGIN GOOGLE IS EXPIRED THEN LOGIN REFREH LOGIN

elif gauth.access_token_expired:
	gauth.Refresh()

# IF LOGIN NOT IN MYCRED.txt FILE IS BLANK THEN YOU MUST LOGIN AGAIN
else:
	gauth.Authorize()


# IF FOUND LOGIN IN mycreds.txt  THEN WRITE TO FILE mycreds.txt

gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)




def main(page:Page):
	page.scroll = "auto"

	# I WANT TO OPERATE CRUD FILE IN FOLDER THAT 
	# SO YOU MUST GET FOLDER ID FROM GDRIVE
	folderId = "14kewUdTIZWgUzmABc38-gHMHU4oSUuLQ"
	allfiles = Column()


	# FOR DELETE FUNCTION FILE
	def deletefile(e):
		youFileId = e.control.data.value
		try:
			# THEN DELETE SELECTED FILE
			drive.CreateFile({"id":youFileId}).Trash()
			# AND IF YOU WANT TO DELETE PERMANNENLY
			# USE .Delete()
			# NEXT SHOW SNACK BAR IF SUCCESS DELETE YOU FILE FROM GDRIVE
			page.snack_bar = SnackBar(
					Text("delete FILE SUCCESS !!"),
					bgcolor="red",
					)
			page.snack_bar.open = True
			page.update()
		except Exception as e:
			print(e)
			print("YOU DELETE FAILED READ THE MESSAGE !!!")


		# YOU MUST SAVE THIS FILE AGAIN FOR RELOAD FLET APPLICATION

	def loadfile():
		# SHOW ALL FILE IN FOLDER ID
		file_list = drive.ListFile({"q":"'14kewUdTIZWgUzmABc38-gHMHU4oSUuLQ' in parents and trashed=false"}).GetList()
		# THEN LOOP FILE
		for x in file_list:
			print(x)
			allfiles.controls.append(
				ListTile(
					leading=Icon(name="description",color="blue"),
					title=Text(x['title']),
					subtitle=Text(x['fileExtension'],size=13),
					trailing = PopupMenuButton(
						icon="more_vert",
						items=[
						PopupMenuItem(text="delete",
						# SEND params ID FILE
						data=Text(x['id']),
						on_click=lambda e:deletefile(e)


							)

						]

						)

					)


				)



	# AND RUN FUNCTION WHEN APP IS READY 
	# LIKE LIFECYCLE IN REACT.js 
	loadfile()


	def uploadnow(e:FilePickerResultEvent):
		for x in e.files:
			try:
				# THIS SCRIPT FOR UPLOAD YOU FILE TO ONLY THIS FOLDER 
				file1 = drive.CreateFile({"title":x.name,"parents":[{"id":folderId}]})
				# THEN WRITE FILE 
				file1.SetContentFile(x.path)
				# X.pATH IS YOU FILE FOR UPLOAD
				file1.Upload()
				print("YOu success Upload guys ... REFRESH YOU APP")
				# THIS OPTIONAL FOR SHOW SNACKBAR
				page.snack_bar = SnackBar(
					Text("You succes Upload !!"),
					bgcolor="green",
					)
				page.snack_bar.open = True
				page.update()
			# AND IF ERROR SHOW EROR IN YOU TERMINAL
			except Exception as e:
				print(e)
				print("FAILED UPLOAD !!!!")


	file_picker = FilePicker(
		on_result=uploadnow
		)
	page.overlay.append(file_picker)
	page.add(
		Column([
		Text("My Flet Drive ",size=30,weight="bold"),
		FloatingActionButton(icon="add",
		bgcolor="blue",
		on_click=lambda e:file_picker.pick_files()
		),
		allfiles 


			])

		)

	# NOW TEST FOR UPLOAD FILE 
	# NOW SUCCESS FOR UPLOAD 
	# NOW SHOW YOU FILE IN LISTTILE
flet.app(target=main)
