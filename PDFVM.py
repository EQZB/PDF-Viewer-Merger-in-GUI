#attempt to make a pdf merger application
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkPDFViewer import tkPDFViewer as pdf
from tkinterdnd2 import DND_FILES, TkinterDnD
from PyPDF2 import PdfMerger
import os
import re

###--------------make tk case-------------------###
root = TkinterDnD.Tk() #for the drop file to work
root.geometry("1000x700+200+100")
root.title("PDF Merger and Viewer")
root.configure(bg="light blue")

###---------grids/entry for view pane-------------###
view_frame=Frame(root, bg="light blue", bd=5, width=400)
view_frame.pack(side=LEFT)
view_entry=Listbox(view_frame, bg="white", width=50, height=2, bd=5)
view_entry.insert(1, "Drag the PDF you want to view here")

###--------register entry box as a drop target---------###
view_entry.drop_target_register(DND_FILES)
view_entry.dnd_bind('<<Drop>>', lambda e: view_entry.insert(tkinter.END, e.data))
view_entry.pack(side=BOTTOM)

##########
dest_folder = '' #for destination folder
##########

###--------grids/listboxes for merge pane-----------###
merge_frame=Frame(root, bg="light blue", bd=5, width=400)
merge_frame.pack(side=RIGHT)
Label(merge_frame, text="Destination Folder").pack(side=BOTTOM)
dest_folder_notif=Listbox(merge_frame, width=40, height=1, bd=1)
dest_folder_notif.pack(side=BOTTOM)
merge_listbox=Listbox(merge_frame, width=50, bd=5)
merge_listbox.insert(1,"Drag the PDFs that you want to merge here:")

###------register the listbox as a drop target-----###
merge_listbox.drop_target_register(DND_FILES)
merge_listbox.dnd_bind('<<Drop>>', lambda e: merge_listbox.insert(tkinter.END, e.data))
merge_listbox.pack(side=BOTTOM)


v2 = None #for view func
m2 = None #for merge func

###--------VIEW functionality (SEARCHING FOR FILES)---------###
def viewpdf():
    #make v2 global
    global v2
    
    filename=filedialog.askopenfilename(initialdir=os.getcwd(),
                                        title="Select PDF File",
                                        filetype=(("PDF File", ".pdf"),
                                                  ("PDF File", ".PDF"),
                                                  ("All File",".txt")))
    
    if filename:
        #destroy old file if it exists
        if v2:
            v2.destroy()
        #create new pdf images  
        v1=pdf.ShowPdf()
        #clear stored images
        v1.img_object_li.clear()
        #set a new pop out window
        newWindow=tkinter.Toplevel(view_frame)
        #store new images
        v2=v1.pdf_view(newWindow, pdf_location=filename, height=50, width=80)
        v2.pack(pady=(0,0))

###------------VIEW functionality (OPENING THE FILE THROUGH ENTRY BOX)-----------###
def viewpdf_eb():
    #make v2 global
    global v2
    
    #get the entry from the view_entry textbox
    filename=view_entry.get(1)
    if filename:
        if filename.endswith(".pdf") == False:
            clean_string=re.sub('[{}]','',filename)
        else:
            clean_string=filename
            
        #destroy old file if it exists
        if v2:
            v2.destroy()
        #create new pdf images  
        v1=pdf.ShowPdf()
        #clear stored images
        v1.img_object_li.clear()
        #set a new pop out window
        newWindow=tkinter.Toplevel(view_frame)
        #store new images
        v2=v1.pdf_view(newWindow, pdf_location=open(clean_string,"r"), height=50, width=80)
        v2.pack(pady=(0,0))

###--------------Delete list in the listbox----------###
def del_list():
    merge_listbox.delete(1,END)

###-----------------Clear PDF view entry-------------###
def clear_view():
    view_entry.delete(1,END)

###-----------------Merge functionality--------------###
def merge_pdf():
    
    merger=PdfMerger()
    
    file_to_merge=[]
    
    click_merge=merge_listbox.get(1,END)
    for pdfs in click_merge:
        #put if statements HERE
        if pdfs.endswith(".pdf") == False:
            clean_string=re.sub('[{}]','',pdfs)
            file_to_merge.append(clean_string)
        else:
            file_to_merge.append(pdfs)
    
    for pdf_file in file_to_merge:
        merger.append(pdf_file)
    
    place_file=dest_folder
    merger.write(place_file + "/" + "Merged-File.pdf")
    merger.close()

    file_to_merge.clear() #to clean the file_to_merge placeholder
    
    #show the pdf after merger
    global m2
    
    filename=place_file + "/" + "Merged-File.pdf"
    
    if filename:
        #destroy old file if it exists
        if m2:
            m2.destroy()
        #create new pdf images  
        m1=pdf.ShowPdf()
        #clear stored images
        m1.img_object_li.clear()
        #set a new pop out window
        newWindow=tkinter.Toplevel(merge_frame)
        #store new images
        m2=m1.pdf_view(newWindow, pdf_location=filename, height=50, width=80)
        m2.pack(pady=(0,0))
    
###----------------------------SET DESTINATION FOLDER-----------------------------###
def set_dest():
    folder=filedialog.askdirectory(initialdir=os.getcwd(), title="Select Destination Folder")
    global dest_folder
    dest_folder = folder
    dest_folder_notif.delete(0)
    dest_folder_notif.insert(1, folder)

###----------------------------set buttons-----------------------------###
view_butt=Button(view_frame, text='SEARCH FOR FILES', command=viewpdf, width=50, bd=5)
view_butt.pack()
view_butt_eb=Button(view_frame, text="VIEW PDF", command=viewpdf_eb, width=50, bd=5)
view_butt_eb.pack(side=BOTTOM)
clear_butt=Button(view_frame, text="CLEAR", command=clear_view, width=50, bd=5)
clear_butt.pack(side=BOTTOM)

merge_butt=Button(merge_frame, text='MERGE', command=merge_pdf, width=50, bd=5)
merge_butt.pack(side=TOP)
merge_del_butt=Button(merge_frame, text='DELETE LIST', command=del_list, width=50, bd=5)
merge_del_butt.pack(side=BOTTOM)
merge_set_dest=Button(merge_frame, text='Set Destination Folder', command=set_dest, width=50, bd=5)
merge_set_dest.pack(side=BOTTOM)

root.mainloop()
