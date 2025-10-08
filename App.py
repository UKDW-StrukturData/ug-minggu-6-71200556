import streamlit as st
from DatabaseManager import excelManager


em = excelManager("dataExcel.xlsx")
options = ["Choose Action","Insert", "Edit", "Delete"]
choice = st.selectbox("Choose an action:", options)
saveChange = st.checkbox("SaveChanges",value=False)

if choice in ("Edit", "Delete"):
    nim = st.text_input("Enter targeted NIM:", key="targetNim")
    if (choice == "Delete"):
        if (sum([1 for i in nim if str(i).isalpha()]) > 0): st.error("Input nim harus angka semua")
        elif st.button("Delete"):
            if (not em.getData("NIM",nim)): st.error("nim not found")
            else:
                em.deleteData(nim,saveChange)
                if (not em.getData("NIM",nim)): st.success("deleted")
            

if (choice in ("Insert","Edit")):
    newNim = st.text_input("Enter New NIM:",key="newNim")
    newName = st.text_input("Enter New Name:",key="newName")
    newGrade = st.text_input("Enter New Grade :", key="newGrade")

    if (choice == "Edit"):
        if st.button("Edit"):
            if (sum([1 for i in newNim if str(i).isalpha()]) > 0): st.error("Input nim harus angka semua")
            elif (sum([1 for i in newName if str(i).isdigit()]) > 0): st.error("Input nama harus Alphabet semua")
            elif (sum([1 for i in newGrade if str(i).isalpha()]) > 0): st.error("Input nilai harus angka semua")
            else:
                msg = em.editData(
                    str(nim),
                    {
                        "Nim": str(newNim).strip(),
                        "Nama": str(newName).strip(),
                        "Nilai": int(newGrade.strip()),
                    },
                    saveChange,
                )
                if "Sukses" in msg:
                    st.success(msg)
                else:
                    st.error(msg)

    if (choice == "Insert"):    
        if (st.button("Insert")):
            if (sum([1 for i in newNim if str(i).isalpha()]) > 0): st.error("Input nim harus angka semua")
            elif (sum([1 for i in newName if str(i).isdigit()]) > 0): st.error("Input nama harus Alphabet semua")
            elif (sum([1 for i in newGrade if str(i).isalpha()]) > 0): st.error("Input nilai harus angka semua")
            else:
                msg = em.insertData(
                    {
                        "Nim": str(newNim).strip(),
                        "Nama": str(newName).strip(),
                        "Nilai": int(newGrade.strip()),
                    },
                    saveChange,
                )
                if "Sukses" in msg:
                    st.success(msg)
                else:
                    st.error(msg)
                                
# TODO: buatkan sistem filter data tabel berdasarkan kolom yang memiliki data angka
option = ["None",">","<","=","<=",">="]
filterSelectBox = st.selectbox("Opsi Filter: ",option)

if (filterSelectBox == "None"):
    st.table(em.getDataFrame()) # tabel biasa
else:
    targetFilterColumn = st.selectbox("Target Column",["NIM","Nilai"]) # pilihan kolom
    filter = st.text_input("Filter Nilai") # input angka filter

    if filter != "":
        df = em.getDataFrame()
        try:
            val int(filter)
            if filterSelectBox == ">":
                st.table(df[df[targetFilterColumn] > val])
            elif filterSelectBox == "<":
                st.table(df[df[targetFilterColumn] < val])
            elif filterSelectBox == "=":
                st.table(df[df[targetFilterColumn] = val])
            elif filterSelectBox == "<=":
                st.table(df[df[targetFilterColumn] <= val])
            elif filterSelectBox == ">=":
                st.table(df[df[targetFilterColumn] >= val])
        
        except:
            st.error("Masukan angka yang valid untuk filter")
